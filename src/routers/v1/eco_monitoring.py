from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.routers.dependensies import get_db
from src.schemas.eco_monitoring import EcoMonitoringRead, EcoMonitoringCreate, EcoMonitoringUpdate
from src.db.models import EcoMonitoring

router_eco_monitoring = APIRouter(prefix="/eco_monitorings", tags=["EcoMonitoring"])


@router_eco_monitoring.post("/add-eco_monitoring", response_model=EcoMonitoringRead)
async def create_eco_monitoring(eco_monitoring: EcoMonitoringCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_eco_monitoring = EcoMonitoring(**eco_monitoring.dict())
        db.add(db_eco_monitoring)
        await db.commit()
        await db.refresh(db_eco_monitoring)
        return db_eco_monitoring
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router_eco_monitoring.get("/", response_model=list[EcoMonitoringRead])
async def read_eco_monitorings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EcoMonitoring))
    eco_monitorings = result.scalars().all()
    return eco_monitorings


@router_eco_monitoring.get("/{eco_monitoring_id}", response_model=EcoMonitoringRead)
async def read_eco_monitoring(eco_monitoring_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EcoMonitoring).where(EcoMonitoring.id == eco_monitoring_id))
    eco_monitoring = result.scalar_one_or_none()
    if not eco_monitoring:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="eco_monitoring не найден")
    return eco_monitoring


@router_eco_monitoring.put("/update-eco_monitoring", response_model=EcoMonitoringRead)
async def update_eco_monitoring(eco_monitoring: EcoMonitoringUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EcoMonitoring).where(EcoMonitoring.id == eco_monitoring.id))
    db_eco_monitoring = result.scalar_one_or_none()
    if not db_eco_monitoring:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EcoMonitoring не найден")

    for key, value in eco_monitoring.dict().items():
        setattr(db_eco_monitoring, key, value)

    await db.commit()
    await db.refresh(db_eco_monitoring)
    return db_eco_monitoring


@router_eco_monitoring.delete("/delete-eco_monitoring/{eco_monitoring_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_eco_monitoring(eco_monitoring_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EcoMonitoring).where(EcoMonitoring.id == eco_monitoring_id)
    )
    db_eco_monitoring = result.scalar_one_or_none()
    if not db_eco_monitoring:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EcoMonitoring не найден")

    await db.delete(db_eco_monitoring)
    await db.commit()
