from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from src.schemas.document import DocumentReadId
from src.schemas.photo import PhotoReadId
from src.schemas.status import StatusRead
from src.schemas.territory import TerritoryReadWithOutData
from src.schemas.track import TrackReadWithOutData
from src.schemas.type_incident import TypeIncidentRead
from src.schemas.user import UserRead


class Point(BaseModel):
    type: str = "Point"
    coordinates: List[float] = Field(..., min_items=2, max_items=3)


class Properties(BaseModel):
    name: str = "Location of eco problem"


class Location(BaseModel):
    type: str = "Feature"
    geometry: Point
    properties: Properties


class EcoProblemBase(BaseModel):
    territory_id: int
    track_id: int
    creator_id: int
    administrator_id: int
    status_id: int
    type_incident_id: int

    title: str
    description: Optional[str]
    classified_type: Optional[dict]
    is_classified: bool = False
    location: Location


class EcoProblemCreate(EcoProblemBase):
    pass


class EcoProblemRead(EcoProblemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: StatusRead
    type_incident: TypeIncidentRead
    creator: UserRead
    administrator: UserRead
    territory: TerritoryReadWithOutData
    track: TrackReadWithOutData
    photos: Optional[list[PhotoReadId]]
    documents: Optional[list[DocumentReadId]]

    class Config:
        orm_mode = True


class EcoProblemReadWithOutJoin(EcoProblemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EcoProblemUpdate(EcoProblemBase):
    id: int

    class Config:
        orm_mode = True
