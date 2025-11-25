from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.crud.user import get_user_by_username
from app.utils.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as s:
        yield s

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = verify_access_token(token)
        username = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    return user
