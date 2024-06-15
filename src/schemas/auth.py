from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    email: str
    password: str = Field(min_length=5)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
