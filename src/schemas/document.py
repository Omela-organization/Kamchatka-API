from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DocumentBase(BaseModel):
    data: Optional[str]


class DocumentRead(DocumentBase):
    id: int
    eco_id: int
    filename: str
    uploaded_at: datetime

    class Config:
        orm_mode = True


class DocumentCreate(DocumentBase):
    eco_id: int
    filename: str


class DocumentUpdate(DocumentBase):
    id: int
    eco_id: int
    filename: str

    class Config:
        orm_mode = True


class DocumentReadId(BaseModel):
    id: int
    eco_id: int
