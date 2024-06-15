from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.models import User
from src.routers.dependensies import get_db
from src.schemas.auth import LoginSchema, TokenSchema
from src.scripts.hash_password import verify_password
from src.scripts.jwt import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_schema = HTTPBearer()

router_auth = APIRouter(prefix="/auth", tags=["Authorization"])


@router_auth.post("/login", status_code=200, response_model=TokenSchema)
async def login(login_data: LoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).
        where(User.email == login_data.email).
        options(joinedload(User.role))
    )
    user_obj = result.scalar_one_or_none()
    if user_obj:
        if verify_password(login_data.password, user_obj.password):
            user_data = {
                "id": user_obj.id,
                "role": user_obj.role.name
            }
            exp_minutes = 60 * 2
            access_token = create_access_token(user=user_data, exp_minutes=exp_minutes)
            refresh_token = create_refresh_token(user=user_data)
            token_type = "Bearer"
            return TokenSchema(access_token=access_token, refresh_token=refresh_token, token_type=token_type)
        else:
            raise HTTPException(status_code=401, detail="No correct password!")
    else:
        raise HTTPException(status_code=404, detail="User doesn't exist!")


@router_auth.post("/user_data_by_token", status_code=200)
async def get_data_by_token(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return decode_access_token(token)


@router_auth.post("/refresh", status_code=200)
async def get_new_access_token(refresh_token: HTTPAuthorizationCredentials):
    token_data = decode_refresh_token(token=refresh_token)
    exp_minutes = 60 * 2
    return {
        "access_token": create_access_token(token_data, exp_minutes=exp_minutes),
        "token_type": "Bearer"
    }
