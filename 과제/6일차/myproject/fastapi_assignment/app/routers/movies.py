# app/routers/movies.py

from typing import Annotated, List

from fastapi import Path, HTTPException, Query, APIRouter, UploadFile

from app.models.movies import MovieModel
from app.schemas.movies import (
    MovieResponse,
    CreateMovieRequest,
    MovieSearchParams,
    MovieUpdateRequest,
)
from app.utils.file import upload_file, delete_file, validate_image_extension

movie_router = APIRouter(prefix="/movies", tags=["movies"])


def _to_response(movie: MovieModel) -> MovieResponse:
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        playtime=movie.playtime,
        genre=movie.genre,
        poster_image_url=movie.poster_image_url,
    )


@movie_router.post("/", response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest):
    movie = MovieModel.create(
        title=data.title,
        playtime=data.playtime,
        genre=data.genre,
    )
    return _to_response(movie)


@movie_router.get("/", response_model=List[MovieResponse])
async def get_movies(query_params: Annotated[MovieSearchParams, Query()] = MovieSearchParams()):
    valid_query = {
        key: value for key, value in query_params.model_dump().items() if value is not None
    }

    movies = MovieModel.all()
    if "title" in valid_query:
        movies = [m for m in movies if valid_query["title"].lower() in m.title.lower()]
    if "genre" in valid_query:
        movies = [m for m in movies if valid_query["genre"].lower() in [g.lower() for g in m.genre]]

    return [_to_response(m) for m in movies]


@movie_router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return _to_response(movie)


@movie_router.patch("/{movie_id}", response_model=MovieResponse)
async def edit_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    valid_params = {key: value for key, value in data.model_dump().items() if value is not None}
    movie.update(**valid_params)
    return _to_response(movie)


@movie_router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.delete()
    return


@movie_router.post("/{movie_id}/poster_image", response_model=MovieResponse, status_code=201)
async def register_poster_image(image: UploadFile, movie_id: int = Path(gt=0)):
    validate_image_extension(image)

    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    prev_image_url = movie.poster_image_url
    try:
        image_url = await upload_file(image, "movies/poster_images")
        movie.poster_image_url = image_url

        if prev_image_url is not None:
            delete_file(prev_image_url)

        return _to_response(movie)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
