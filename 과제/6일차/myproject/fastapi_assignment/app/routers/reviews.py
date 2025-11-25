from fastapi import APIRouter

review_router = APIRouter(prefix="/reviews", tags=["reviews"])

@review_router.get("/")
async def list_reviews():
    return {"message": "review list (dummy)"}
