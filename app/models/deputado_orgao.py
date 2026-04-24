from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class DeputadoOrgao(Base):
    __tablename__ = "deputado_orgao"

    id = Column(Integer, primary_key=True, index=True)
    id_orgao = Column(Integer, nullable=True)
    nome = Column(String, nullable=True)           # Nome do Órgão (ex: Comissão de Educação)
    sigla = Column(String, nullable=True)          # Sigla do Órgão
    nome_deputado = Column(String, nullable=True)  # Este é o campo que eu uso principalmente para as buscas por nome
    cargo = Column(String, nullable=True)          # Cargo do deputado (Titular, Suplente...)
    sigla_uf = Column(String, nullable=True)       # Estado (UF) pelo qual o deputado foi eleito
    data_inicio = Column(Date, nullable=True)      # Data em que ele entrou no órgão
    data_final = Column(Date, nullable=True)       # Data em que ele saiu (se ainda estiver, fica vazio)
    sigla_partido = Column(String, nullable=True)  # Partido do deputado