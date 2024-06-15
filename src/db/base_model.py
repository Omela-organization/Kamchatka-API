from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/EcoKamchatka"
# DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/EcoKamchatka'
# async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# async session
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def drop_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    await engine.dispose()
