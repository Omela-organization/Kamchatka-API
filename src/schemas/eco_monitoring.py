from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class EcoMonitoringCreate(BaseModel):
    territory_id: int
    track_id: int
    type_data: str
    data: dict = {}
    params: Optional[dict] = {}

    class Config:
        orm_mode = True


class EcoMonitoringRead(EcoMonitoringCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class EcoMonitoringUpdate(EcoMonitoringCreate):
    id: int

    class Config:
        orm_mode = True
