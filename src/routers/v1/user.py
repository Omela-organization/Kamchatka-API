from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from src.db.models import User
from src.routers.dependensies import get_db
from src.schemas.user import UserRead, UserCreate, UserUpdate

router_user = APIRouter(prefix="/users", tags=["User"])


@router_user.post("/add-user", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    result = await db.execute(
        select(User).
        where(User.id == new_user.id).
        options(joinedload(User.role))
    )
    new_user = result.scalars().first()
    return new_user


@router_user.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).
        where(User.id == user_id).
        options(joinedload(User.role))
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router_user.get("/", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).
        options(joinedload(User.role))
    )
    users = result.scalars().all()
    return users


@router_user.put("/update-user", response_model=UserRead)
async def update_user(user: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).
        where(User.id == user.id).
        options(joinedload(User.role))
    )
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(existing_user, key, value)

    await db.commit()
    await db.refresh(existing_user)
    return existing_user


@router_user.delete("/delete-user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
