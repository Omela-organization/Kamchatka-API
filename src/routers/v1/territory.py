from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status as status

from src.routers.dependensies import get_db
from src.schemas.territory import TerritoryCreate, TerritoryUpdate, TerritoryRead
from src.db.models import Territory
from src.schemas.territory_track import TerritoryReadWithTracks

router_territory = APIRouter(prefix="/territories", tags=["Territory"])


@router_territory.post("/add-territory", response_model=TerritoryRead)
async def create_territory(territory: TerritoryCreate, db: AsyncSession = Depends(get_db)):
    new_territory = Territory(**territory.dict())
    db.add(new_territory)
    await db.commit()
    await db.refresh(new_territory)
    return new_territory


@router_territory.get("/", response_model=list[TerritoryRead])
async def get_territories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Territory))
    territory = result.scalars().all()
    return territory


@router_territory.get("/with_tracks/{territory_id}", response_model=TerritoryReadWithTracks)
async def get_territory_by_id_with_tracks(territory_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Territory).
        where(Territory.id == territory_id).
        options(joinedload(Territory.tracks))
    )
    territory = result.scalars().first()
    return territory


@router_territory.get("/{territory_id}", response_model=TerritoryRead)
async def get_territory(territory_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Territory).where(Territory.id == territory_id))
    territory = result.scalars().first()
    if not territory:
        raise HTTPException(status_code=404, detail="Territory not found")
    return territory


@router_territory.put("/update-territory", response_model=TerritoryRead)
async def update_territory(territory: TerritoryUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Territory).where(Territory.id == territory.id))
    db_territory = result.scalars().first()
    if not db_territory:
        raise HTTPException(status_code=404, detail="Territory not found")

    for key, value in territory.dict().items():
        setattr(db_territory, key, value)

    await db.commit()
    await db.refresh(db_territory)
    return db_territory


@router_territory.delete("/delete-territory/{territory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_territory(territory_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Territory).where(Territory.id == territory_id))
    territory = result.scalars().first()
    if not territory:
        raise HTTPException(status_code=404, detail="Territory not found")

    await db.delete(territory)
    await db.commit()
