from fastapi import APIRouter

from .endpoints import artigo, usuario
from core.configs import settings

api_router = APIRouter()

api_router.include_router(artigo.router, prefix="/artigos", tags=["artigos"])
api_router.include_router(usuario.router, prefix="/usuarios", tags=["usuarios"])
