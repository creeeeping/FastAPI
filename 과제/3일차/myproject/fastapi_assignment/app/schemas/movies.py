# app/schemas/movies.py

from typing import List

from pydantic import BaseModel, Field


class CreateMovieRequest(BaseModel):
    title: str
    playtime: int
    genre: List[str]


class MovieResponse(BaseModel):
    id: int
    title: str
    playtime: int
    genre: List[str]


class MovieSearchParams(BaseModel):
    title: str | None = None
    genre: str | None = None


class MovieUpdateRequest(BaseModel):
    title: str | None = None
    playtime: int | None = Field(default=None, gt=0)
    genre: List[str] | None = None
