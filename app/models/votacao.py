from sqlalchemy import Column, String, DateTime, Integer, Text
from app.core.database import Base

class Votacao(Base):
    __tablename__ = "votacao"

    # Minhas colunas de Identificação
    id = Column(Integer, primary_key=True, index=True)
    id_votacao = Column(String, index=True) 
    
    # Informações do Deputado que votou
    id_deputado = Column(String, index=True)
    nome = Column(String, index=True)
    sigla_partido = Column(String)
    sigla_uf = Column(String)
    id_legislatura = Column(Integer)
    
    # O voto que o deputado deu (Sim, Não, Abstenção, etc)
    voto = Column(String)
    
    # Contexto de quando a votação aconteceu
    data_hora = Column(DateTime, nullable=True, index=True)        # Data e hora principal da votação
    data_registro = Column(DateTime, nullable=True)                # Data em que o voto foi registrado
    horario_registro = Column(String, nullable=True)               # Horário exato do registro
    
    # Onde a votação ocorreu (Plenário, Comissões, etc)
    id_orgao = Column(String, nullable=True, index=True)
    sigla_orgao = Column(String, nullable=True)
    
    # O que estava sendo votado
    id_ultima_proposicao = Column(String, nullable=True, index=True) # O ID oficial do PL/PEC
    descricao_ultima_proposicao = Column(Text, nullable=True)        # Título da proposta que estava em pauta
    descricao_votacao = Column(Text, nullable=True)                  # O assunto específico desta votação
    
    # O resultado final (Ex: "Aprovado", "Rejeitado")
    aprovacao = Column(String, nullable=True)