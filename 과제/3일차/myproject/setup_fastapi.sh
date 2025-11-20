#!/bin/bash

PROJECT="fastapi_assignment"

echo "�� FastAPI 프로젝트 생성 시작: $PROJECT"

# 생성할 디렉토리 구조
mkdir -p $PROJECT/app/models
mkdir -p $PROJECT/app/schemas
mkdir -p $PROJECT/app/routers

# -------------------------
# main.py 생성
# -------------------------
cat << 'EOF' > $PROJECT/main.py
from fastapi import FastAPI
from app.routers import users, movies

app = FastAPI(
    title="FastAPI Assignment",
    description="Sample FastAPI Project Structure",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(movies.router)

@app.get("/")
def root():
    return {"message": "FastAPI Assignment Running!"}
EOF

# -------------------------
# __init__.py (app)
# -------------------------
echo "" > $PROJECT/app/__init__.py

# -------------------------
# models/users.py
# -------------------------
cat << 'EOF' > $PROJECT/app/models/users.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
EOF

# -------------------------
# models/movies.py
# -------------------------
cat << 'EOF' > $PROJECT/app/models/movies.py
from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    director: str
EOF

# -------------------------
# schemas/users.py
# -------------------------
cat << 'EOF' > $PROJECT/app/schemas/users.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
EOF

# -------------------------
# schemas/movies.py
# -------------------------
cat << 'EOF' > $PROJECT/app/schemas/movies.py
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
EOF

# -------------------------
# routers/users.py
# -------------------------
cat << 'EOF' > $PROJECT/app/routers/users.py
from fastapi import APIRouter
from app.schemas.users import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

fake_users = []
user_id = 1

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global user_id
    new_user = {"id": user_id, **user.dict()}
    user_id += 1
    fake_users.append(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users():
    return fake_users
EOF

# -------------------------
# routers/movies.py
# -------------------------
cat << 'EOF' > $PROJECT/app/routers/movies.py
from fastapi import APIRouter
from app.schemas.movies import MovieCreate, MovieResponse

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
EOF

# -------------------------
# routers/__init__.py
# -------------------------
echo "" > $PROJECT/app/routers/__init__.py

echo "🎉 FastAPI 프로젝트 생성 완료!"
echo "👉 프로젝트 폴더: $PROJECT"
echo "👉 실행: uvicorn main:app --reload"

