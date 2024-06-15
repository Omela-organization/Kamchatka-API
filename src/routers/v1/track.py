from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, Load
from starlette import status

from src.db.models import Track, Territory
from src.routers.dependensies import get_db
from src.schemas.territory_track import TrackReadWithTerritory
from src.schemas.track import TrackCreate, TrackUpdate, TrackRead

router_track = APIRouter(prefix="/tracks", tags=["Track"])


@router_track.post("/add-track", response_model=TrackRead)
async def create_track(track: TrackCreate, db: AsyncSession = Depends(get_db)):
    new_track = Track(**track.dict())
    db.add(new_track)
    await db.commit()
    await db.refresh(new_track)
    return new_track


@router_track.get("/{track_id}", response_model=TrackReadWithTerritory)
async def get_track(track_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Track).
        where(Track.id == track_id).
        options(joinedload(Track.territory).options(Load(Territory).load_only(Territory.id, Territory.name, Territory.description)))
    )
    track = result.scalars().first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router_track.get("/", response_model=list[TrackReadWithTerritory])
async def get_tracks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Track).
        options(joinedload(Track.territory))
    )
    tracks = result.scalars().all()
    return tracks


@router_track.put("/update-track", response_model=TrackRead)
async def update_track(track: TrackUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Track).where(Track.id == track.id))
    existing_track = result.scalars().first()
    if not existing_track:
        raise HTTPException(status_code=404, detail="Track not found")

    for key, value in track.dict().items():
        setattr(existing_track, key, value)

    await db.commit()
    await db.refresh(existing_track)
    return existing_track


@router_track.delete("/delete-track/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_track(track_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Track).where(Track.id == track_id))
    track = result.scalars().first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    await session.delete(track)
    await session.commit()
