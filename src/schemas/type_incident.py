from pydantic import BaseModel


class TypeIncidentBase(BaseModel):
    name: str


class TypeIncidentCreate(TypeIncidentBase):
    pass


class TypeIncidentRead(TypeIncidentBase):
    id: int

    class Config:
        orm_mode = True


class TypeIncidentUpdate(TypeIncidentRead):
    pass
