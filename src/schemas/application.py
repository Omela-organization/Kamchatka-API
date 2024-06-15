from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from src.schemas.user import UserRead


class Visitor(BaseModel):
    surname: str
    name: str
    patronymic: str
    birthday: str
    citizenship: str
    refistration_region: str
    gender: str
    passport: str
    email: str
    phone: str


class ApplicationBase(BaseModel):
    name: str
    creator_id: int
    administrator_id: int
    territory_id: int
    track_id: int
    start_date: date
    end_date: date
    car_plate: Optional[str]
    is_permitted: bool = False
    visitors: list[Visitor]


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationRead(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    creator: UserRead
    administrator: UserRead

    class Config:
        orm_mode = True


class ApplicationReadWithOutJoin(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ApplicationUpdate(ApplicationBase):
    id: int

    class Config:
        orm_mode = True
