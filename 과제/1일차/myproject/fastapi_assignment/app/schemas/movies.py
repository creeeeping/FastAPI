from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    director: str

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str

    class Config:
        from_attributes = True
