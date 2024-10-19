from pydantic import BaseModel
from datetime import date


class GetUser(BaseModel):
    username: str

    class Config:
        extra = "forbid"


class GetNewWeight(BaseModel):
    weight: int
    date: date

    class Config:
        extra = "forbid"


class GetloginData(BaseModel):
    password: str
    height: float

    class Config:
        extra = "forbid"
