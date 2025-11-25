# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.users import user_router
from app.routers.movies import movie_router
from app.routers.reviews import review_router
from app.routers.likes import like_router

app = FastAPI(title="FastAPI Assignment", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user_router)
app.include_router(movie_router)
app.include_router(review_router)
app.include_router(like_router)


@app.get("/")
def root():
    return {"message": "FastAPI Assignment Running"}
