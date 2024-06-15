from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

from src.schemas.role import RoleRead


class UserCreate(BaseModel):
    email: str
    password: Optional[str] = Field(min_length=5)
    role_id: int


class UserUpdate(BaseModel):
    id: int
    email: str
    name: Optional[str]
    surname: Optional[str]
    phone: Optional[str]
    role_id: int

    class Config:
        orm_mode = True


class UserRead(UserUpdate):
    created_at: datetime
    updated_at: datetime
    role: RoleRead

    class Config:
        orm_mode = True
