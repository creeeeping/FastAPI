from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

async def get_user_by_username(db:AsyncSession, username:str):
    q=await db.execute(select(User).where(User.username==username))
    return q.scalars().first()

async def create_user(db:AsyncSession, payload:UserCreate):
    u=User(username=payload.username, email=payload.email, password_hash=get_password_hash(payload.password))
    db.add(u)
    await db.commit()
    await db.refresh(u)
    return u
