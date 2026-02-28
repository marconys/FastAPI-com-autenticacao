from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router

app = FastAPI(
    title="FastAPI Authentication",
    description="API para estudar autenticação",
    version="1.0.0",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)


    """
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzcyODkwOTcwLCJpYXQiOjE3NzIyODYxNzAsInN1YiI6Im1tb3VyYUBnbWFpbC5jb20ifQ.Wg-bxKtLU-lTgkSyuPP1eZSaF6EhqNgLl193ZTaUPgI",
    "token_type": "bearer"
    """
