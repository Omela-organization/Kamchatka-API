from typing import Optional

from pydantic import BaseModel


class FeedBackBase(BaseModel):
    territory_id: int
    track_id: int
    creator_id: int
    rate_painting: Optional[int]
    rate_facilities: Optional[int]
    rate_purity: Optional[int]
    rate_expectations: Optional[int]


class FeedBackCreate(FeedBackBase):
    pass


class FeedBackRead(FeedBackBase):
    id: int

    class Config:
        orm_mode = True


class FeedBackUpdate(FeedBackRead):
    pass
