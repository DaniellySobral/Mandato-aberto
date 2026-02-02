from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class DeputadoOrgao(Base):
    __tablename__ = "deputado_orgao"

    id = Column(Integer, primary_key=True, index=True)
    id_orgao = Column(Integer, nullable=True)
    nome = Column(String, nullable=True)          # Nome do Órgão (Comissão)
    sigla = Column(String, nullable=True)         # Sigla do Órgão
    nome_deputado = Column(String, nullable=True)  # O campo importante para a busca
    cargo = Column(String, nullable=True)          # Cargo (Titular, Suplente...)
    sigla_uf = Column(String, nullable=True)       # Estado
    data_inicio = Column(Date, nullable=True)     # Data Início
    data_final = Column(Date, nullable=True)       # Data Fim
    sigla_partido = Column(String, nullable=True)  # Partido