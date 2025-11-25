from fastapi import FastAPI

from app.models.users import UserModel
from app.models.movies import MovieModel
from app.routers.users import router as user_router
from app.routers.movies import movie_router


app = FastAPI(title="FastAPI Assignment - Forms & File Upload")


# Seed some dummy data on startup
@app.on_event("startup")
async def startup_event():
    UserModel.create_dummy()
    MovieModel.create_dummy()


app.include_router(user_router)
app.include_router(movie_router)


@app.get("/")
async def root():
    return {"message": "FastAPI assignment with file upload is running."}
