from pytz import timezone

from typing import Optional, List

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha

from pydantic import EmailStr

# Endppoint para autenticação, onde o usuário irá enviar o username e password para obter o token
oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuarios/login")


async def autenticar_usuario(
    email: EmailStr, senha: str, db: AsyncSession
) -> Optional[UsuarioModel]:
    async with db as session:
        # Busca o usuário pelo email
        query = select(UsuarioModel).where(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: Optional[UsuarioModel] = result.scalars().unique().one_or_none()

    # Verifica se o usuário existe e se a senha é válida
    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha):
        return None

    return usuario


def criar_token(tipo_token: str, tempo_expiracao: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}

    sp = timezone("America/Sao_Paulo")
    expira = datetime.now(tz=sp) + tempo_expiracao

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    # https://jwt.io
    return criar_token(
        tipo_token="access_token",
        tempo_expiracao=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
