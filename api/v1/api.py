from fastapi import APIRouter

from .endpoints import artigo, usuario

api_router = APIRouter()

api_router.include_router(artigo.router)
api_router.include_router(usuario.router)
