from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings

from models.usuario_model import UsuarioModel


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:

    async with Session() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)
) -> UsuarioModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    query = select(UsuarioModel).where(UsuarioModel.email == token_data.username)
    result = await db.execute(query)
    usuario: Optional[UsuarioModel] = result.scalars().unique().one_or_none()

    if usuario is None:
        raise credentials_exception
    return usuario
