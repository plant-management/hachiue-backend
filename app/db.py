from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker #,declarative_base
from sqlalchemy.ext.declarative import declarative_base #こっちのほうがいいかも

ASYNK_DB_URL = "mysql+aiomysql://root@db:3306/hachiue_db?charset=utf8"

async_engine = create_async_engine(ASYNK_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False,autoflush=False,bind=async_engine,class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session