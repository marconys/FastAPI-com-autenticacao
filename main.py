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
