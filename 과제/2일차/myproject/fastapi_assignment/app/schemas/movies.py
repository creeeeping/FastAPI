from pydantic import BaseModel, Field
from typing import List, Annotated

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
    playtime: Annotated[int, Field(gt=0)] | None = None
    genre: List[str] | None = None
