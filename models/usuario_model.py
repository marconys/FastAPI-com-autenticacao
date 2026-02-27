from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.configs import settings


class UsuarioModel(settings.DB_BASE):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=True)
    sobrenome = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    eh_admin = Column(Boolean, default=False)

    artigos = relationship(
        "ArtigoModel",
        back_populates="criador",
        cascade="all, delete-orphan",
        lazy="joined",
    )
