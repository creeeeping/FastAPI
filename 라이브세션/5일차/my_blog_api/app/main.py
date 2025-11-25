from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import Base, engine
from app.dependencies import get_db
from app.routers import auth as auth_router
from app.routers import user as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Rebuilt API", lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(auth_router.router)

@app.get("/")
async def health(db: AsyncSession = Depends(get_db)):
    r = await db.execute(text("SELECT 1"))
    return {"db_connected": r.scalar()==1}
