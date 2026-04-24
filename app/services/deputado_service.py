from sqlalchemy.orm import Session
from app.models.deputado_orgao import DeputadoOrgao
from app.schemas.schemas import DeputadoOrgaoResponse
from sqlalchemy import func, or_, and_
from app.models.votacao import Votacao 


def buscar_orgaos_por_nome(db: Session, termo_busca: str):
    """
    Aqui eu filtro o banco de dados buscando deputados que contenham o termo digitado.
    Utilizo o 'ilike' para que a busca ignore letras maiúsculas e minúsculas.
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
    Nesta função eu executo a busca avançada no banco, aplicando todos os filtros que o usuário preencheu na API.
    """
    query = db.query(DeputadoOrgao)

    # 1. Aplico os filtros de texto simples (nome, estado, partido)
    if nome:
        query = query.filter(DeputadoOrgao.nome_deputado.ilike(f"%{nome}%"))
    
    if uf:
        # Transformo a sigla em maiúsculo para garantir que ache mesmo se digitarem 'sp' ou 'Sp'
        query = query.filter(DeputadoOrgao.sigla_uf == uf.upper())
        
    if partido:
        query = query.filter(DeputadoOrgao.sigla_partido == partido.upper())

    # 2. Lógica do recorte temporal (Ano Início e Fim)
    # Eu só aplico essa regra se o usuário tiver preenchido ambos os anos na busca
    if ano_inicio and ano_fim:
        # Converto os anos para o formato de data do banco para poder comparar
        # A ideia aqui é buscar mandatos que estavam ativos em algum momento dentro desse intervalo de tempo
        data_limit_inferior = f"{ano_inicio}-01-01"
        data_limit_superior = f"{ano_fim}-12-31"
        
        query = query.filter(
            or_(
                # Cenário A: O mandato tem data de fim e ocorreu dentro do período que estou buscando
                and_(
                    DeputadoOrgao.data_inicio <= data_limit_superior,
                    DeputadoOrgao.data_final >= data_limit_inferior
                ),
                # Cenário B: O mandato ainda está em andamento (data_final é vazia)
                # e ele começou antes do limite final da minha busca
                and_(
                    DeputadoOrgao.data_final.is_(None),
                    DeputadoOrgao.data_inicio <= data_limit_superior
                )
            )
        )

    return query.all()


def analisa_votos_deputado(db: Session, nome: str, ano: int):
    """
    Nesta função eu busco os votos por nome e ano. Como podem existir vários deputados com o mesmo nome (ex: "Silva"),
    eu agrupo e separo a contagem de Sim/Não/Abstenção para cada deputado individualmente.
    """
    # 1. Filtro pelo nome e uso strftime do SQLite para pegar só o ano da coluna data_hora
    query = db.query(Votacao).filter(
        Votacao.nome.ilike(f"%{nome}%"),
        func.strftime('%Y', Votacao.data_hora) == str(ano)
    )
    
    votos_encontrados = query.all()
    
    # 2. Crio um mapa para padronizar as palavras que vêm do banco para o formato da nossa API
    mapa_votos = {
        "Sim": "sim",
        "Não": "nao",
        "Abstenção": "abstencao",
        "Obstrução": "obstrucao"
    }
    
    # Este dicionário vai servir como meu "fichário" para separar os votos por ID do deputado
    agrupado = {}
    
    for v in votos_encontrados:
        id_dep = v.id_deputado
        # Se eu ainda não criei a "gaveta" desse deputado, crio agora com os contadores zerados
        if id_dep not in agrupado:
            agrupado[id_dep] = {
                "id_deputado": id_dep,
                "nome": v.nome,
                "partido": v.sigla_partido,
                "uf": v.sigla_uf,
                "resumo": {
                    "sim": 0,
                    "nao": 0,
                    "abstencao": 0,
                    "obstrucao": 0,
                    "total": 0
                },
                "primeiras_votacoes": []
            }
            
        chave_limpa = mapa_votos.get(v.voto)
        if chave_limpa in agrupado[id_dep]["resumo"]:
            agrupado[id_dep]["resumo"][chave_limpa] += 1
            
        agrupado[id_dep]["resumo"]["total"] += 1
        
        # Guardo até 5 exemplos de votação para esse deputado
        if len(agrupado[id_dep]["primeiras_votacoes"]) < 5:
            agrupado[id_dep]["primeiras_votacoes"].append({
                "data": v.data_hora,
                "voto": v.voto,
                "id_votacao": v.id_votacao
            })
            
    return list(agrupado.values())