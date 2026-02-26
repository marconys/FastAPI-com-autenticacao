import asyncio

from core.configs import settings
from core.database import engine

from models.__all_models import *


async def main():
    try:
        async with engine.begin() as conn:
            print("Criando tabelas...")
            await conn.run_sync(settings.DB_BASE.metadata.drop_all)
            await conn.run_sync(settings.DB_BASE.metadata.create_all)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
