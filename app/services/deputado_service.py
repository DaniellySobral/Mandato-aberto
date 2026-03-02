from sqlalchemy.orm import Session
from app.models.deputado_orgao import DeputadoOrgao
from app.schemas.schemas import DeputadoOrgaoResponse
from sqlalchemy import func
from app.models.votacao import Votacao 


def buscar_orgaos_por_nome(db: Session, termo_busca: str):
    """
    Filtra o banco buscando deputados que contenham o termo.
    O 'ilike' faz a busca ser insensível a maiúsculas/minúsculas.
    """
    resultados = db.query(DeputadoOrgao).filter(
        DeputadoOrgao.nome_deputado.ilike(f"%{termo_busca}%")
    ).all()

 
def buscar_deputados_avancada(
    db: Session, 
    nome: str = None, 
    uf: str = None, 
    partido: str = None, 
    ano_inicio: int = None, 
    ano_fim: int = None
):
    """
    Executa a busca no banco aplicando todos os filtros selecionados.
    """
    query = db.query(DeputadoOrgao)

    # 1. Filtros de Texto Simples
    if nome:
        query = query.filter(DeputadoOrgao.nome_deputado.ilike(f"%{nome}%"))
    
    if uf:
        # Transforma em maiúsculo para garantir que ache 'sp', 'SP', 'Sp'
        query = query.filter(DeputadoOrgao.sigla_uf == uf.upper())
        
    if partido:
        query = query.filter(DeputadoOrgao.sigla_partido == partido.upper())

    # 2. Lógica de Recorte Temporal (Ano Início e Fim)
    # Só aplica se o usuário mandou os dois anos
    if ano_inicio and ano_fim:
        # Converte os anos inteiros (ex: 2015) para datas de string para comparar no banco
        # Busca mandatos que estavam vivos em algum momento entre 01/01/Inicio e 31/12/Fim
        data_limit_inferior = f"{ano_inicio}-01-01"
        data_limit_superior = f"{ano_fim}-12-31"
        
        query = query.filter(
            or_(
                # Cenário A: O mandato tem data fim definida e cruza o período
                and_(
                    DeputadoOrgao.data_inicio <= data_limit_superior,
                    DeputadoOrgao.data_final >= data_limit_inferior
                ),
                # Cenário B: O mandato está em andamento (data_final é NULL/vazia)
                # E começou antes do fim do período pesquisado
                and_(
                    DeputadoOrgao.data_final.is_(None),
                    DeputadoOrgao.data_inicio <= data_limit_superior
                )
            )
        )

    return query.all()


def analisa_votos_deputado(db: Session, nome: str, ano: int):
    """
    Busca todos os votos de um deputado em um ano específico e conta Sim/Não/Abstenção.
    """
    # 1. Filtra pelo nome (insensível) e extrai o ano da data_hora
    # No SQLite usamos strftime para pegar só o ano da data
    query = db.query(Votacao).filter(
        Votacao.nome.ilike(f"%{nome}%"),
        func.strftime('%Y', Votacao.data_hora) == str(ano)
    )
    
    votos_encontrados = query.all()
    
    # 2. Conta os votos na mão (mais fácil de entender)
    resumo = {
        "Sim": 0,
        "Não": 0,
        "Abstenção": 0,
        "Obstrução": 0,
        "Total": len(votos_encontrados)
    }
    
    detalhes = [] # Para guardar exemplos das votações
    
    for v in votos_encontrados:
        # Se o voto existir no nosso dicionário de resumo, soma 1
        if v.voto in resumo:
            resumo[v.voto] += 1
        
        # Guarda alguns detalhes para mostrar na tela
        detalhes.append({
            "data": v.data_hora,
            "voto": v.voto,
            "id_votacao": v.id_votacao
        })
        
    return resumo, detalhes