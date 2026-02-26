from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaArtigos, UsuarioSchemaUpdate, UsuarioSchemaCreate

from core.deps import get_session, get_current_user
from core.security import generate_password_hash
from core.auth import autenticar_usuario, criar_token_acesso


router = APIRouter()

# GET Logado
@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

# POST / Signup
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_signup(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=generate_password_hash(usuario.senha),
        eh_admin=usuario.eh_admin
    )
    try:
        db.add(novo_usuario)
        await db.commit()
        await db.refresh(novo_usuario)
        return novo_usuario
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar salvar o usuario no banco de dados.",
        )

# GET Usuarios
@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    try:
        query = select(UsuarioModel)
        result = await db.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().all()
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar buscar os usuarios no banco de dados.",
        )

# GET Usuario by id
@router.get("/{usuario_id}", response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    try:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await db.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado."
            )
        return usuario
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar buscar o usuario no banco de dados.",
        )

# PUT Update Usuario
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(
    usuario_id: int,
    usuario: UsuarioSchemaUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    try:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await db.execute(query)
        usuario_update: UsuarioModel = result.scalars().first()
        if not usuario_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado."
            )
        if usuario_update.usuario_id != usuario_logado.id and not usuario_logado.eh_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para atualizar este usuario.",
            )
        if usuario.nome:
            usuario_update.nome = usuario.nome
        if usuario.sobrenome:
            usuario_update.sobrenome = usuario.sobrenome
        if usuario.email:
            usuario_update.email = usuario.email
        if usuario.senha:
            usuario_update.senha = generate_password_hash(usuario.senha)
        if usuario.eh_admin:
            usuario_update.eh_admin = usuario.eh_admin
        await db.commit()
        await db.refresh(usuario_update)
        return usuario_update
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar atualizar o usuario no banco de dados.",
        )

# DELETE Usuario
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    try:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await db.execute(query)
        usuario: UsuarioModel = result.scalars().first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado."
            )

        if usuario_logado.eh_admin is False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para deletar este usuario.",
            )

        await db.delete(usuario)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao tentar deletar o usuario no banco de dados.",
        )


# POST Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar_usuario(email=form_data.username, senha=form_data.password, db=db)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha invalidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)


