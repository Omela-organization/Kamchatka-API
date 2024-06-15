from pydantic import BaseModel
from typing import Optional


class TrackCreate(BaseModel):
    name: str
    length: Optional[float] = None
    time_passing_track: Optional[float] = None
    type_track: Optional[str] = None
    basic_recreational_capacity: Optional[int] = None
    territory_id: int
    data: Optional[dict] = None


class TrackUpdate(BaseModel):
    id: int
    name: str
    length: Optional[float] = None
    time_passing_track: Optional[float] = None
    type_track: Optional[str] = None
    basic_recreational_capacity: Optional[int] = None
    territory_id: int
    data: Optional[dict] = None

    class Config:
        orm_mode = True


class TrackRead(TrackUpdate):
    pass


class TrackReadWithOutData(BaseModel):
    id: int
    name: str
    length: Optional[float] = None
    time_passing_track: Optional[float] = None
    type_track: Optional[str] = None
    basic_recreational_capacity: Optional[int] = None
    territory_id: int

    class Config:
        orm_mode = True