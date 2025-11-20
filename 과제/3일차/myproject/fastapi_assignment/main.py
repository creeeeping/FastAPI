# main.py

from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query

from app.models.users import UserModel
from app.models.movies import MovieModel
from app.schemas.users import (
    UserCreateRequest,
    UserUpdateRequest,
    UserSearchParams,
)
from app.schemas.movies import (
    CreateMovieRequest,
    MovieResponse,
    MovieSearchParams,
    MovieUpdateRequest,
)

app = FastAPI(title="FastAPI Assignment")

# 더미 데이터 생성 (원하면 주석 처리)
UserModel.create_dummy()
MovieModel.create_dummy()

# -------------------------------------------------
# 1. 유저 생성 API (POST /users)
# -------------------------------------------------


@app.post("/users")
async def create_user(data: UserCreateRequest):
    # 비밀번호는 과제에 없으니 임시로 username 기반 문자열 사용
    user = UserModel.create(
        username=data.username,
        password=f"{data.username}_pw",
        age=data.age,
        gender=data.gender.value,
    )
    return user.id


# -------------------------------------------------
# 2. 전체 유저 조회 (GET /users)
# -------------------------------------------------


@app.get("/users")
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result


# -------------------------------------------------
# 3. 특정 유저 조회 (GET /users/{user_id})
# -------------------------------------------------


@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------------------------------------------------
# 4. 유저 부분 수정 (PATCH /users/{user_id})
# -------------------------------------------------


@app.patch("/users/{user_id}")
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.update(**data.model_dump())
    return user


# -------------------------------------------------
# 5. 유저 삭제 (DELETE /users/{user_id})
# -------------------------------------------------


@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.delete()
    return {"detail": f"User: {user_id}, Successfully Deleted."}


# -------------------------------------------------
# 6. 유저 검색 (GET /users/search)
# -------------------------------------------------


@app.get("/users/search")
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {
        key: value
        for key, value in query_params.model_dump().items()
        if value is not None
    }
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404, detail="No users matched")
    return filtered_users


# =================================================
# 영화 API
# =================================================

# 1. 영화 등록 (POST /movies)


@app.post("/movies", response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest):
    movie = MovieModel.create(**data.model_dump())
    return movie


# 2. 영화 리스트 + 검색 (GET /movies)


@app.get("/movies", response_model=list[MovieResponse], status_code=200)
async def get_movies(query_params: Annotated[MovieSearchParams, Query()]):
    valid_query = {
        key: value
        for key, value in query_params.model_dump().items()
        if value is not None
    }

    if valid_query:
        return MovieModel.filter(**valid_query)

    return MovieModel.all()


# 3. 특정 영화 상세 조회 (GET /movies/{movie_id})


@app.get("/movies/{movie_id}", response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# 4. 특정 영화 수정 (PATCH /movies/{movie_id})


@app.patch("/movies/{movie_id}", response_model=MovieResponse, status_code=200)
async def edit_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.update(**data.model_dump())
    return movie


# 5. 특정 영화 삭제 (DELETE /movies/{movie_id})


@app.delete("/movies/{movie_id}", status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.delete()
    return
