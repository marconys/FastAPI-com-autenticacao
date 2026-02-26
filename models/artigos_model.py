from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class ArtigoModel(settings.DB_BASE):
    __tablename__ = "artigos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    url_fonte = Column(String(255), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    criador = relationship("UsuarioModel", back_populates="artigos", lazy="joined")
