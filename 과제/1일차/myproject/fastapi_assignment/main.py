from fastapi import FastAPI
from fastapi_assignment.app.routers import users, movies

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
