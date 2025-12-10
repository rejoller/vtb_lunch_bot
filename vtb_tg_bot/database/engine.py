from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import os
from database.models import Base
import logging

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_HOST = os.getenv('DB_HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')




DBURL=f'postgresql+psycopg://{USER}:{PASSWORD}@{DB_HOST}:{port}/{database}'



DBURL=f'postgresql+psycopg://vtb_lunch_bot:vtb_lunch_bot@{DB_HOST}:{port}/vtb_lunch_bot'
print(DBURL)

logging.info(DBURL)

engine = create_async_engine(DBURL, echo=False, pool_size=15, pool_timeout=30, pool_recycle=900)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print('создана бд')
        
        
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print('удалена бд')
