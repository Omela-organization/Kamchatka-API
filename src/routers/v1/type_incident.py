from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.routers.dependensies import get_db
from src.schemas.type_incident import TypeIncidentRead, TypeIncidentCreate, TypeIncidentUpdate
from src.db.models import TypeIncident

router_type_incident = APIRouter(prefix="/type_incidents", tags=["Type Incident"])


@router_type_incident.post("/add-type-incident", response_model=TypeIncidentRead)
async def create_type_incident(type_incident: TypeIncidentCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_type_incident = TypeIncident(**type_incident.dict())
        db.add(db_type_incident)
        await db.commit()
        await db.refresh(db_type_incident)
        return db_type_incident
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Тип инцидентов с названием {type_incident.name} уже есть в базе"
        )


@router_type_incident.get("/", response_model=list[TypeIncidentRead])
async def read_type_incidents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TypeIncident))
    type_incidents = result.scalars().all()
    return type_incidents


@router_type_incident.get("/{type_incident_id}", response_model=TypeIncidentRead)
async def read_type_incident(type_incident_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TypeIncident).where(TypeIncident.id == type_incident_id))
    type_incident = result.scalar_one_or_none()
    if not type_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тип инцидента не найден")
    return type_incident


@router_type_incident.put("/update-type-incident", response_model=TypeIncidentRead)
async def update_type_incident(type_incident: TypeIncidentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TypeIncident).where(TypeIncident.id == type_incident.id))
    db_type_incident = result.scalar_one_or_none()
    if not db_type_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тип инцидента не найден")

    for key, value in type_incident.dict().items():
        setattr(db_type_incident, key, value)

    await db.commit()
    await db.refresh(db_type_incident)
    return db_type_incident


@router_type_incident.delete("/delete-type-incident/{type_incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_type_incident(type_incident_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TypeIncident).where(TypeIncident.id == type_incident_id)
    )
    db_type_incident = result.scalar_one_or_none()
    if not db_type_incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тип инцидента не найден")

    await db.delete(db_type_incident)
    await db.commit()
