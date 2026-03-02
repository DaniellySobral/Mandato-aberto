from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.schemas import DeputadoOrgaoResponse
from app.services.deputado_service import buscar_deputados_avancada
from app.services.deputado_service import analisa_votos_deputado
from typing import Dict, List, Any

router = APIRouter()

# --- SUA NOVA ROTA AVANÇADA ---
@router.get("/deputados/advanced_search", response_model=list[DeputadoOrgaoResponse])
def advanced_search(
    nome: Optional[str] = Query(None, description="Nome do deputado (parte do nome)"),
    uf: Optional[str] = Query(None, description="Sigla do Estado (ex: SP)"),
    partido: Optional[str] = Query(None, description="Sigla do Partido (ex: PT)"),
    ano_inicio: Optional[int] = Query(None, ge=1990, le=2030, description="Ano Início"),
    ano_fim: Optional[int] = Query(None, ge=1990, le=2030, description="Ano Fim"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para consulta com múltiplos filtros.
    Exemplo de URL: 
    /deputados/advanced_search?nome=Silva&uf=SP&ano_inicio=2015&ano_fim=2020
    """
    resultados = buscar_deputados_avancada(db, nome, uf, partido, ano_inicio, ano_fim)
    return resultados


@router.get("/deputados/analise_votos")
def analisar_votos(
    nome: str = Query(..., description="Nome do Deputado"),
    ano: int = Query(..., description="Ano para análise (ex: 2024)"),
    db: Session = Depends(get_db)
):
    """
    Retorna um resumo de quantos Sim/Não/Abstenção o deputado teve no ano.
    Exemplo: /deputados/analise_votos?nome=Alice&ano=2024
    """
    resumo, detalhes = analisa_votos_deputado(db, nome, ano)
    
    return {
        "deputado": nome,
        "ano": ano,
        "resumo": resumo,
        "primeiras_votacoes": detalhes[:5] # Mostra só as 5 primeiras como exemplo
    }