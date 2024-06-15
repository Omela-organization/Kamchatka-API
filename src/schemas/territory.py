from pydantic import BaseModel
from typing import Optional


class TerritoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    data: Optional[dict] = None


class TerritoryRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    data: Optional[dict] = None

    class Config:
        orm_mode = True


class TerritoryReadWithOutData(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class TerritoryUpdate(TerritoryRead):
    pass
