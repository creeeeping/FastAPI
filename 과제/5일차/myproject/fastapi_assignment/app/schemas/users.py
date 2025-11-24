# app/schemas/users.py

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class UserCreate(BaseModel):
    username: str
    password: str
    age: int = Field(gt=0)
    gender: GenderEnum


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[GenderEnum] = None


class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    gender: GenderEnum
    profile_image_url: str | None = None
