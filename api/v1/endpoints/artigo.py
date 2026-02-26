from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigos_model import ArtigoModel
from models.usuario_model import UsuarioModel

from schemas.artigo_schema import ArtigoSchema

from core.deps import get_session, get_current_user

router = APIRouter(prefix="/artigos", tags=["artigos"])


# POST New Artigo
@router.post("/", response_model=ArtigoSchema, status_code=status.HTTP_201_CREATED)
async def post_artigo(
    artigo: ArtigoSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    novo_artigo = ArtigoModel(**artigo.model_dump(), usuario_id=usuario_logado.id)
    try:
        db.add(novo_artigo)
        await db.commit()
        await db.refresh(novo_artigo)
        return novo_artigo
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar salvar o artigo no banco de dados.",
        )


# GET All Artigos
@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    try:
        query = await db.execute(select(ArtigoModel))
        return query.scalars().all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar buscar os artigos no banco de dados.",
        )


# GET Artigo by id
@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    try:
        query = await db.execute(select(ArtigoModel).where(ArtigoModel.id == artigo_id))
        artigo = query.scalars().first()
        if not artigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado."
            )
        return artigo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar buscar o artigo no banco de dados.",
        )


# PUT Update Artigo
@router.put(
    "/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED
)
async def put_artigo(
    artigo_id: int,
    artigo: ArtigoSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    try:
        query = await db.execute(select(ArtigoModel).where(ArtigoModel.id == artigo_id))
        artigo_update = query.scalars().first()

        if not artigo_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado."
            )
        if artigo_update.usuario_id != usuario_logado.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para atualizar este artigo.",
            )

        if artigo.titulo:
            artigo_update.titulo = artigo.titulo
        if artigo.descricao:
            artigo_update.descricao = artigo.descricao
        if artigo.url_fonte:
            artigo_update.url_fonte = artigo.url_fonte

        await db.commit()
        await db.refresh(artigo_update)

        return artigo_update
    except HTTPException as e:
        raise e

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar atualizar o artigo no banco de dados.",
        )


# DELETE Artigo
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(
    artigo_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    try:
        query = await db.execute(select(ArtigoModel).where(ArtigoModel.id == artigo_id))
        artigo = query.scalars().first()
        if not artigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado."
            )
        await db.delete(artigo)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar deletar o artigo no banco de dados.",
        )
