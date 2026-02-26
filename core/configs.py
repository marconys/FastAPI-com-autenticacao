from typing import Any, List

from pydantic import BaseModel, AnyUrl

from sqlalchemy.ext.declarative import declarative_base

# cria a base para os modelos do SQLAlchemy
Base: Any = declarative_base()


class Settings(BaseModel):

    API_V1_STR: str = "/api/v1"
    DB_URL: AnyUrl = "postgresql+asyncpg://postgres:123456@localhost:5433/faculdadedb"
    DB_BASE: Any = Base
    HOST: str = "localhost"
    PORT: int = 8000

    JWT_SECRET_KEY: str = ("KQnqsJRoAylhv4MgfrznxRwJgOMZujFf_gkT7bynz9o",)
    """   
     
    import secrets
    token = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = ("HS256",)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias,

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


# Instância global das configurações
settings = Settings()
