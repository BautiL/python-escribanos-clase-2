from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/tramite_db"

engine = create_async_engine(DATABASE_URL, 
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass