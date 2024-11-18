import os


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .models import Base
from .config import settings
from .orm_commands import orm_create_categories
from .banners import categories

ASYNC_URI = settings.SQLALCHEMY_DATABASE_URI.replace('postgresql', 'postgresql+asyncpg')

engine = create_async_engine(ASYNC_URI, echo=True)
sessionmaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with sessionmaker() as session:
        await orm_create_categories(session, categories)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)