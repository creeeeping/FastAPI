from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user, get_user_by_username
from app.dependencies import get_db, get_current_user

router=APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead)
async def register(payload:UserCreate, db:AsyncSession=Depends(get_db)):
    if await get_user_by_username(db, payload.username):
        raise HTTPException(status_code=409, detail="exists")
    return await create_user(db, payload)

@router.get("/{username}", response_model=UserRead)
async def read(username:str, db:AsyncSession=Depends(get_db), current=Depends(get_current_user)):
    u=await get_user_by_username(db, username)
    if not u: raise HTTPException(404)
    return u
