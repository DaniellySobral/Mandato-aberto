import basedosdados as bd
import sys
from app.core.database import SessionLocal, Base, engine
from app.models.votacao import Votacao
from sqlalchemy.exc import IntegrityError
from datetime import datetime


BILLING_PROJECT_ID = "mandato-aberto-dados"

def carregar_votacoes_bd():
    print("🔌 Conectando ao Base dos Dados (BigQuery)...")

        # QUERY COMPLETA no banco (Pegando todos os dados importantes para as votações)
    query = """
      SELECT
        v.data as data_hora,
        v.data_registro as data_registro,
        v.horario_registro as horario_registro,
        
        vp.voto as voto,
        vp.id_deputado as id_deputado,
        vp.nome as nome,
        vp.sigla_partido as sigla_partido,
        vp.sigla_uf as sigla_uf,
        vp.id_legislatura as id_legislatura,
        vp.id_votacao as id_votacao,
        
        v.id_orgao as id_orgao,
        v.sigla_orgao as sigla_orgao,
        
        v.id_ultima_proposicao as id_ultima_proposicao,
        v.descricao_ultima_proposicao as descricao_ultima_proposicao,
        v.descricao as descricao_votacao,
        
        v.aprovacao as aprovacao
        
      FROM `basedosdados.br_camara_dados_abertos.votacao_parlamentar` AS vp
      LEFT JOIN `basedosdados.br_camara_dados_abertos.votacao` AS v
        ON vp.id_votacao = v.id_votacao
      WHERE v.data >= '2023-01-01'
      LIMIT 50000
    """

    try:
        # Executo a query e já trago o resultado no formato de DataFrame do Pandas
        df = bd.read_sql(query=query, billing_project_id=BILLING_PROJECT_ID)
        print(f"✅ Sucesso! Foram retornadas {len(df)} linhas do Base dos Dados.")
        
    except Exception as e:
        print(f"❌ Erro na conexão com Base dos Dados: {e}")
        print("Dica: Verifique se seu billing_id está correto e se você tem internet.")
        sys.exit()

    # Crio a tabela no banco de dados local caso ela ainda não exista
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    print("💾 Salvando no banco local (SQLite)...")

    try:
        # Uso o pandas para fazer o 'bulk insert' direto no banco de dados, o que deixa o processo bem rápido
        # A configuração 'if_exists="append"' garante que eu adicione as novas linhas aos dados já existentes
        df.to_sql(
            'votacao', 
            con=engine, 
            if_exists='append', 
            index=False
        )
        print("✅ Dados salvos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao salvar no banco local: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Criei essa confirmação antes de rodar para evitar custos desnecessários com a nuvem do BigQuery
    confirmar = input("Isso vai consultar o BigQuery. Tem certeza? (s/n): ")
    if confirmar.lower() == 's':
        carregar_votacoes_bd()
    else:
        print("Cancelado.")