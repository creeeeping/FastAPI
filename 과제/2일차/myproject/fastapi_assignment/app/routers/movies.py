from fastapi import APIRouter
from fastapi_assignment.app.schemas.movies import MovieCreate, MovieResponse

router = APIRouter(prefix="/movies", tags=["Movies"])

fake_movies = []
movie_id = 1


@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate):
    global movie_id
    new_movie = {"id": movie_id, **movie.dict()}
    movie_id += 1
    fake_movies.append(new_movie)
    return new_movie


@router.get("/", response_model=list[MovieResponse])
def get_movies():
    return fake_movies
