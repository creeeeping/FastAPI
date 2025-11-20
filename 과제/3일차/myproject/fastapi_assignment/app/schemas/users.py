# app/schemas/users.py
from enum import Enum
from typing import Optional, Annotated
from pydantic import BaseModel, Field


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class UserCreateRequest(BaseModel):
    username: str
    age: int
    gender: GenderEnum


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None


class UserSearchParams(BaseModel):
    class Config:
        extra = "forbid"

    username: Optional[str] = None
    age: Annotated[Optional[int], Field(gt=0)] = None
    gender: Optional[GenderEnum] = None
