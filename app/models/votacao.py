from sqlalchemy import Column, String, DateTime, Integer, Text
from app.core.database import Base

class Votacao(Base):
    __tablename__ = "votacao"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    id_votacao = Column(String, index=True) 
    
    # Dados do Deputado
    id_deputado = Column(String, index=True)
    nome = Column(String, index=True)
    sigla_partido = Column(String)
    sigla_uf = Column(String)
    id_legislatura = Column(Integer)
    
    # Dados do Voto Individual
    voto = Column(String)
    
    # Dados da Votação (Contexto)
    data_hora = Column(DateTime, nullable=True, index=True)       # Data/Hora principal
    data_registro = Column(DateTime, nullable=True)                # Data de registro
    horario_registro = Column(String, nullable=True)               # Horário exato
    
    # Dados do Órgão (Onde votou)
    id_orgao = Column(String, nullable=True, index=True)
    sigla_orgao = Column(String, nullable=True)
    
    # Dados da Proposta (O que foi votado)
    id_ultima_proposicao = Column(String, nullable=True, index=True) # ID do PL/PEC
    descricao_ultima_proposicao = Column(Text, nullable=True)        # Título da Proposta
    descricao_votacao = Column(Text, nullable=True)                  # O assunto da votação
    
    # Resultado
    aprovacao = Column(String, nullable=True) # Ex: "Aprovado", "Rejeitado"