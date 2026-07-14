from datetime import datetime
from app.models.votacao import Votacao
from app.services.deputado_service import analisa_votos_deputado

def test_deputado_sem_mudancas_partido(db_session):
    # 1. Cria um deputado fictício com votos apenas em um partido no ano de 2024
    votos = [
        Votacao(
            id_votacao="1",
            id_ultima_proposicao="101",
            id_deputado="123",
            nome="Deputado Teste",
            sigla_partido="PT",
            sigla_uf="SP",
            voto="Sim",
            data_hora=datetime(2024, 1, 10, 14, 0),
            aprovacao="1"
        ),
        Votacao(
            id_votacao="2",
            id_ultima_proposicao="102",
            id_deputado="123",
            nome="Deputado Teste",
            sigla_partido="PT",
            sigla_uf="SP",
            voto="Não",
            data_hora=datetime(2024, 2, 15, 16, 0),
            aprovacao="0"
        )
    ]
    db_session.add_all(votos)
    db_session.commit()

    # 2. Executa a análise para o ano de 2024
    resultados = analisa_votos_deputado(db_session, "Teste", 2024)

    # 3. Validações
    assert len(resultados) == 1
    dep = resultados[0]
    assert dep["id_deputado"] == "123"
    assert dep["nome"] == "Deputado Teste"
    assert dep["partido_atual"] == "PT"
    assert dep["total_mudancas_partido"] == 0
    assert dep["partidos_anteriores"] == []
    assert dep["uf"] == "SP"
    
    # Resumo quantitativo
    assert dep["resumo"]["sim"] == 1
    assert dep["resumo"]["nao"] == 1
    assert dep["resumo"]["total"] == 2

    # Detalhes das proposições
    assert len(dep["proposicoes_votadas_sim"]) == 1
    assert dep["proposicoes_votadas_sim"][0]["id_proposicao"] == "101"
    assert dep["proposicoes_votadas_sim"][0]["aprovada_na_camara"] is True

    assert len(dep["proposicoes_votadas_nao"]) == 1
    assert dep["proposicoes_votadas_nao"][0]["id_proposicao"] == "102"
    assert dep["proposicoes_votadas_nao"][0]["aprovada_na_camara"] is False


def test_deputado_com_mudancas_partido(db_session):
    # 1. Cria histórico de votos cronológico com trocas de partido (PL -> PATRIOTA -> PRD)
    votos = [
        Votacao(
            id_votacao="1",
            id_ultima_proposicao="201",
            id_deputado="456",
            nome="Deputada Mudanca",
            sigla_partido="PL",
            sigla_uf="RJ",
            voto="Sim",
            data_hora=datetime(2023, 5, 1, 10, 0),
            aprovacao="1"
        ),
        Votacao(
            id_votacao="2",
            id_ultima_proposicao="202",
            id_deputado="456",
            nome="Deputada Mudanca",
            sigla_partido="PATRIOTA",
            sigla_uf="RJ",
            voto="Sim",
            data_hora=datetime(2023, 9, 1, 14, 0),
            aprovacao="0"
        ),
        Votacao(
            id_votacao="3",
            id_ultima_proposicao="203",
            id_deputado="456",
            nome="Deputada Mudanca",
            sigla_partido="PRD",
            sigla_uf="RJ",
            voto="Não",
            data_hora=datetime(2024, 2, 1, 11, 0),
            aprovacao="1"
        )
    ]
    db_session.add_all(votos)
    db_session.commit()

    # 2. Executa a análise para o ano de 2024
    resultados = analisa_votos_deputado(db_session, "Mudanca", 2024)

    assert len(resultados) == 1
    dep = resultados[0]
    assert dep["id_deputado"] == "456"
    assert dep["partido_atual"] == "PRD"
    assert dep["total_mudancas_partido"] == 2
    assert dep["partidos_anteriores"] == ["PL", "PATRIOTA"]
    
    # No ano de 2024, ela só votou 1 vez (voto "Não")
    assert dep["resumo"]["sim"] == 0
    assert dep["resumo"]["nao"] == 1
    assert dep["resumo"]["total"] == 1
    assert len(dep["proposicoes_votadas_sim"]) == 0
    assert len(dep["proposicoes_votadas_nao"]) == 1
