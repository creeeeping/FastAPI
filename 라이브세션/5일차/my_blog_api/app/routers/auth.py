from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.dependencies import get_db
from app.crud.user import get_user_by_username
from app.utils.security import verify_password, create_access_token

router=APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login(f:OAuth2PasswordRequestForm=Depends(), db:AsyncSession=Depends(get_db)):
    u=await get_user_by_username(db, f.username)
    if not u or not verify_password(f.password, u.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"access_token":create_access_token(u.username, timedelta(minutes=60)), "token_type":"bearer"}
