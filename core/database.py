from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from core.configs import settings

# Cria o engine assíncrono do SQLAlchemy
engine: AsyncEngine = create_async_engine(str(settings.DB_URL), echo=True)

# Cria a fábrica de sessões assíncronas
Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)
