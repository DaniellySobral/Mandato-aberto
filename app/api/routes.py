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
    Aqui eu criei uma rota para permitir consultas avançadas, aceitando vários filtros ao mesmo tempo.
    Exemplo de uso na URL: 
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
    Nesta rota eu retorno a contagem de votos (Sim/Não/Abstenção) já agrupada por deputado.
    Se a busca encontrar mais de um deputado com o mesmo nome (ex: vários deputados chamados "Silva"),
    eu devolvo a contagem separada para cada um deles.
    Exemplo de uso: /deputados/analise_votos?nome=Silva&ano=2024
    """
    resultados = analisa_votos_deputado(db, nome, ano)
    
    return {
        "termo_busca": nome,
        "ano": ano,
        "deputados_encontrados": resultados
    }