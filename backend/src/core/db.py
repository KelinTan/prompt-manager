from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import get_settings

settings = get_settings()
ASYNC_DATABASE_URL = f"mysql+aiomysql://{settings.db_user}:{settings.db_password}@{settings.db_host}?charset=utf8mb4"
SYNC_DATABASE_URL = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}?charset=utf8mb4"
# 同步引擎
engine = create_engine(
    SYNC_DATABASE_URL,
    pool_pre_ping=True,  # 检测连接是否可用
    pool_recycle=3600,  # 连接回收时间 (1 hour, increased from 30 min for better reuse)
    pool_size=20,  # 连接池大小 (increased for better concurrency)
    max_overflow=30,  # 超出连接池大小外最多创建的连接数
    echo=False,  # 是否打印SQL日志
    pool_timeout=30,  # 从池中获取连接的超时时间
)
# 异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,  # Increased for better connection reuse
    pool_size=20,  # Increased pool size for async operations
    max_overflow=30,
    echo=False,
    pool_timeout=30,  # Connection acquisition timeout
)


def get_session():
    return Session(engine)


async def get_async_session():
    session = AsyncSession(async_engine, expire_on_commit=False)
    try:
        yield session
    except Exception as e:
        await session.rollback()
        await session.close()
        raise e
    finally:
        await session.close()
