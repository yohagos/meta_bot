from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from configs import load_settings

settings = load_settings()

SYNC_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_URL}/{settings.DB_NAME}"
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)


ASYNC_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_URL}/{settings.DB_NAME}"
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,  
    expire_on_commit=False
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,  
    class_=AsyncSession,
    expire_on_commit=False
)

def create_tables():
    SQLModel.metadata.create_all(sync_engine)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all(async_engine))


def get_sync_session():
    with SessionLocal() as session:
        yield session

def get_sync_engine():
    return sync_engine


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session

def get_async_engine():
    return async_engine