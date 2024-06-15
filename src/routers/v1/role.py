from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.routers.dependensies import get_db
from src.schemas.role import RoleRead, RoleCreate, RoleUpdate
from src.db.models import Role

router_role = APIRouter(prefix="/roles", tags=["Role"])


@router_role.post("/add-role", response_model=RoleRead)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_role = Role(**role.dict())
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)
        return db_role
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Роль с названием {role.name} уже есть в базе"
        )


@router_role.get("/", response_model=list[RoleRead])
async def read_roles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return roles


@router_role.get("/{role_id}", response_model=RoleRead)
async def read_role(role_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")
    return role


@router_role.put("/update-role", response_model=RoleRead)
async def update_role(role: RoleUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).where(Role.id == role.id))
    db_role = result.scalar_one_or_none()
    if not db_role:
        raise HTTPException(status_code=404, detail="Роль не найдена")

    for key, value in role.dict().items():
        setattr(db_role, key, value)

    await db.commit()
    await db.refresh(db_role)
    return db_role


@router_role.delete("/delete-role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    db_role = result.scalar_one_or_none()
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")

    await db.delete(db_role)
    await db.commit()
