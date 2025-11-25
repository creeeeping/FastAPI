from fastapi import APIRouter

like_router = APIRouter(prefix="/likes", tags=["likes"])

@like_router.get("/")
async def list_likes():
    return {"message": "likes list (dummy)"}
