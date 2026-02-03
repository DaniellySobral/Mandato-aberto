from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import DeputadoOrgaoResponse
from app.services.deputado_service import buscar_orgaos_por_nome

router = APIRouter()

@router.get("/deputados/search", response_model=list[DeputadoOrgaoResponse])
def search_deputados(nome: str, db: Session = Depends(get_db)):
    """
    URL de Exemplo: /deputados/search?nome=Rodrigo
    """
    orgaos = buscar_orgaos_por_nome(db, nome)
    return orgaos