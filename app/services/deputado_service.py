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
    Além disso, calculo o histórico de mudanças de partido (total_mudancas_partido e partidos_anteriores)
    e listo as proposições votadas de forma detalhada para Sim e Não.
    """
    # 1. Encontro todos os IDs de deputados distintos que correspondem ao nome pesquisado e possuem votos no ano
    ids_deputados = db.query(Votacao.id_deputado).filter(
        Votacao.nome.ilike(f"%{nome}%"),
        func.strftime('%Y', Votacao.data_hora) == str(ano)
    ).distinct().all()
    
    ids_deputados = [r[0] for r in ids_deputados if r[0]]
    
    resultados = []
    
    # 2. Para cada deputado encontrado, processamos seu histórico completo
    for id_dep in ids_deputados:
        # Buscamos todos os votos históricos dele ordenados por data e hora (do mais antigo ao mais recente)
        votos_historicos = db.query(Votacao).filter(
            Votacao.id_deputado == id_dep
        ).order_by(Votacao.data_hora.asc()).all()
        
        if not votos_historicos:
            continue
            
        # Rastreando mudanças de partido cronologicamente
        partidos_sequencia = []
        for v in votos_historicos:
            if v.sigla_partido:
                partido = v.sigla_partido.strip()
                if not partidos_sequencia or partidos_sequencia[-1] != partido:
                    partidos_sequencia.append(partido)
                    
        # Filtramos as votações apenas do ano especificado
        votos_ano = [v for v in votos_historicos if v.data_hora and v.data_hora.year == ano]
        
        mapa_votos = {
            "Sim": "sim",
            "Não": "nao",
            "Abstenção": "abstencao",
            "Obstrução": "obstrucao"
        }
        
        resumo = {
            "sim": 0,
            "nao": 0,
            "abstencao": 0,
            "obstrucao": 0,
            "total": 0
        }
        
        proposicoes_votadas_sim = []
        proposicoes_votadas_nao = []
        
        # Como o nome ou UF podem ter variações de grafia, pegamos o registro mais recente
        nome_deputado = votos_historicos[-1].nome
        sigla_uf = votos_historicos[-1].sigla_uf
        
        for v in votos_ano:
            chave_limpa = mapa_votos.get(v.voto)
            if chave_limpa in resumo:
                resumo[chave_limpa] += 1
            resumo["total"] += 1
            
            # Verificando se a proposição foi aprovada na Câmara
            aprovada_na_camara = None
            if v.aprovacao in ["1", 1, "Aprovado"]:
                aprovada_na_camara = True
            elif v.aprovacao in ["0", 0, "Rejeitado"]:
                aprovada_na_camara = False
                
            prop_info = {
                "id_proposicao": v.id_ultima_proposicao,
                "descricao": v.descricao_votacao or v.descricao_ultima_proposicao or "Sem descrição disponível",
                "aprovada_na_camara": aprovada_na_camara,
                "data": v.data_hora
            }
            
            if v.voto == "Sim":
                proposicoes_votadas_sim.append(prop_info)
            elif v.voto == "Não":
                proposicoes_votadas_nao.append(prop_info)
                
        resultados.append({
            "id_deputado": id_dep,
            "nome": nome_deputado,
            "partido_atual": partidos_sequencia[-1] if partidos_sequencia else None,
            "total_mudancas_partido": len(partidos_sequencia) - 1 if len(partidos_sequencia) > 0 else 0,
            "partidos_anteriores": partidos_sequencia[:-1] if len(partidos_sequencia) > 0 else [],
            "uf": sigla_uf,
            "resumo": resumo,
            "proposicoes_votadas_sim": proposicoes_votadas_sim,
            "proposicoes_votadas_nao": proposicoes_votadas_nao
        })
        
    return resultados