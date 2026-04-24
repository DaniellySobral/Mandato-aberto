import pandas as pd
import sys
from app.core.database import SessionLocal, Base, engine
from app.models.deputado_orgao import DeputadoOrgao
from sqlalchemy.exc import IntegrityError

def carregar_csv():
    # 1. Defino o caminho onde o arquivo CSV está salvo no meu projeto
    caminho_arquivo = './data/br_camara_dados_abertos_orgao_deputado.csv'
    
    print("Iniciando a leitura do CSV...")
    
    try:
        # 2. Utilizo o Pandas para ler o CSV ignorando linhas quebradas
        df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8', on_bad_lines='warn', dtype=str)
        print(f"Total de linhas lidas: {len(df)}")
        
    except FileNotFoundError:
        print("❌ Erro: O arquivo CSV não foi encontrado na pasta './data/'. Verifique o nome e o local.")
        sys.exit()
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo CSV: {e}")
        sys.exit()

    # 3. Garanto que as tabelas do banco estejam criadas
    Base.metadata.create_all(bind=engine)
    
    # 4. Abro a conexão com o banco de dados
    db = SessionLocal()
    
    registros_para_salvar = []
    erros_encontrados = 0
    total_inserido = 0

    print("Processando os dados...")

    # 5. Percorro o arquivo do Pandas linha por linha
    for index, row in df.iterrows():
        try:
            # Tratamento de datas
            inicio = pd.to_datetime(row['data_inicio'], errors='coerce')
            final = pd.to_datetime(row['data_final'], errors='coerce')
            
            if pd.notna(inicio): inicio = inicio.date()
            if pd.notna(final): final = final.date()

            # Crio um registro baseado no meu modelo do SQLAlchemy
            registro = DeputadoOrgao(
                id_orgao=row.get('id_orgao'),
                nome=row.get('nome'),
                sigla=row.get('sigla'),
                nome_deputado=row.get('nome_deputado'),
                cargo=row.get('cargo'),
                sigla_uf=row.get('sigla_uf'),
                data_inicio=inicio,
                data_final=final,
                sigla_partido=row.get('sigla_partido')
            )
            registros_para_salvar.append(registro)

            # Para não sobrecarregar o banco, eu salvo as informações em lotes de 500
            if len(registros_para_salvar) >= 500:
                try:
                    db.bulk_save_objects(registros_para_salvar)
                    db.commit()
                    total_inserido += len(registros_para_salvar)
                    print(f"✅ Salvo lote. Total processado até agora: {index + 1} linhas")
                    registros_para_salvar = []
                except IntegrityError as e:
                    # Se eu encontrar algum erro de duplicidade, eu desfaço o lote (rollback) e ignoro
                    print(f"⚠️ Erro de integridade (duplicidade?) no lote {index + 1}: {e}")
                    db.rollback()
                    erros_encontrados += len(registros_para_salvar)
                    registros_para_salvar = []
                except Exception as e:
                    # Tratamento para quaisquer outros erros inesperados
                    print(f"❌ Erro geral no lote {index + 1}: {e}")
                    db.rollback()
                    erros_encontrados += len(registros_para_salvar)
                    registros_para_salvar = []

        except Exception as e:
            print(f"⚠️ Erro na linha {index + 2}: {e} (Linha ignorada)")
            erros_encontrados += 1
            continue

    # 6. Salvo qualquer registro que tenha sobrado no final do loop
    if registros_para_salvar:
        try:
            db.bulk_save_objects(registros_para_salvar)
            db.commit()
            total_inserido += len(registros_para_salvar)
        except Exception as e:
            print(f"⚠️ Erro ao salvar o último lote: {e}")
            db.rollback()
            erros_encontrados += len(registros_para_salvar)

    print(f"\n✅ Processo concluído!")
    print(f"Total de registros inseridos no banco: {total_inserido}")
    if erros_encontrados > 0:
        print(f"Total de registros ignorados por erro: {erros_encontrados}")
    
    db.close()

if __name__ == "__main__":
    carregar_csv()