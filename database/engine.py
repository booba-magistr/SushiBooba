import os


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .models import Base

engine = create_async_engine(os.getenv('SQLITE_DB'), echo=True)
sessionmaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)