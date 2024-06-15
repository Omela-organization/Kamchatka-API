from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status as starlette_status

from src.routers.dependensies import get_db
from src.schemas.status import StatusRead, StatusCreate, StatusUpdate
from src.db.models import Status

router_status = APIRouter(prefix="/statuses", tags=["Status"])


@router_status.post("/add-status", response_model=StatusRead)
async def create_status(status: StatusCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_status = Status(**status.dict())
        db.add(db_status)
        await db.commit()
        await db.refresh(db_status)
        return db_status
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Статус с названием {status.name} уже есть в базе"
        )


@router_status.get("/", response_model=list[StatusRead])
async def read_statuses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Status))
    statuses = result.scalars().all()
    return statuses


@router_status.get("/{status_id}", response_model=StatusRead)
async def read_status(status_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Status).where(Status.id == status_id))
    status = result.scalar_one_or_none()
    if not status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Статус не найден")
    return status


@router_status.put("/update-status", response_model=StatusRead)
async def update_status(status: StatusUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Status).where(Status.id == status.id))
    db_status = result.scalar_one_or_none()
    if not db_status:
        raise HTTPException(status_code=404, detail="Статус не найден")

    for key, value in status.dict().items():
        setattr(db_status, key, value)

    await db.commit()
    await db.refresh(db_status)
    return db_status


@router_status.delete("/delete-status/{status_id}", status_code=starlette_status.HTTP_204_NO_CONTENT)
async def delete_status(status_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Status).where(Status.id == status_id)
    )
    db_status = result.scalar_one_or_none()
    if not db_status:
        raise HTTPException(status_code=starlette_status.HTTP_404_NOT_FOUND, detail="Статус не найден")

    await db.delete(db_status)
    await db.commit()
