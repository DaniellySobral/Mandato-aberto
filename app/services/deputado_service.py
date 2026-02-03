from sqlalchemy.orm import Session
from app.models.deputado_orgao import DeputadoOrgao
from app.schemas.schemas import DeputadoOrgaoResponse

def buscar_orgaos_por_nome(db: Session, termo_busca: str):
    """
    Filtra o banco buscando deputados que contenham o termo.
    O 'ilike' faz a busca ser insensível a maiúsculas/minúsculas.
    """
    resultados = db.query(DeputadoOrgao).filter(
        DeputadoOrgao.nome_deputado.ilike(f"%{termo_busca}%")
    ).all()

    return resultados