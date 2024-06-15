from typing import Optional

from src.schemas.track import TrackRead
from src.schemas.territory import TerritoryRead, TerritoryReadWithOutData


class TerritoryReadWithTracks(TerritoryRead):
    tracks: Optional[list[TrackRead]] = []


class TrackReadWithTerritory(TrackRead):
    territory: TerritoryReadWithOutData

    class Config:
        orm_mode = True
