from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PhotoBase(BaseModel):
    data: Optional[str]


class PhotoRead(PhotoBase):
    id: int
    eco_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True


class PhotoCreate(PhotoBase):
    eco_id: int


class PhotoUpdate(PhotoRead):
    pass


class PhotoReadId(BaseModel):
    id: int
    eco_id: int
