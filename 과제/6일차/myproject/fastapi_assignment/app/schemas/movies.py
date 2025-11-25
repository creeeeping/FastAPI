# app/schemas/movies.py

from typing import List, Any

from pydantic import BaseModel, Field


class CreateMovieRequest(BaseModel):
    title: str
    playtime: int = Field(gt=0)
    genre: List[str]


class MovieResponse(BaseModel):
    id: int
    title: str
    playtime: int
    genre: List[str]
    poster_image_url: str | None = None


class MovieSearchParams(BaseModel):
    title: str | None = None
    genre: str | None = None


class MovieUpdateRequest(BaseModel):
    title: str | None = None
    playtime: int | None = Field(default=None, gt=0)
    genre: List[str] | None = None
