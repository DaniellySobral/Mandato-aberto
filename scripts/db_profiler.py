import basedosdados as bd
import argparse

def inspecionar_tabela(nome_tabela, billing_project_id):
    """
    Conecta ao BigQuery e retorna as colunas disponíveis na tabela.
    """
    print(f"🔍 Conectando ao BigQuery para inspecionar a tabela: {nome_tabela}")
    
    # Pega apenas 1 linha para descobrir a estrutura (colunas e tipos)
    query = f"SELECT * FROM `{nome_tabela}` LIMIT 1"
    
    try:
        df = bd.read_sql(query=query, billing_project_id=billing_project_id)
        
        print("\n" + "="*50)
        print(f"✅ TABELA ENCONTRADA: {nome_tabela}")
        print("="*50)
        
        print(f"\nTotal de colunas: {len(df.columns)}\n")
        
        print("📋 LISTA DE COLUNAS DISPONÍVEIS:")
        print("-" * 50)
        
        # Mostra nome da coluna e o tipo de dado (String, Int, Date, etc.)
        for i, col in enumerate(df.columns):
            tipo_dado = str(df[col].dtype)
            print(f"{i+1:02}. {col:<40} | Tipo: {tipo_dado}")
            
        print("-" * 50)
        print("\n💡 DICAS:")
        print("1. Copie os nomes das colunas para criar seu Modelo (app/models).")
        print("2. Use esses nomes exatamente iguais na query do seu Ingestor.")
        
    except Exception as e:
        print(f"\n❌ Erro ao acessar a tabela: {e}")
        print("Verifique se o nome da tabela está correto (ex: basedosdados.br_camara_dados_abertos.votacao)")

if __name__ == "__main__":
    # Configuração para receber argumentos do terminal
    parser = argparse.ArgumentParser(description="Ferramenta para descobrir colunas de tabelas no Base dos Dados.")
    
    parser.add_argument("--tabela", required=True, help="Nome completo da tabela (ex: basedosdados.br_camara_dados_abertos.proposicao)")
    parser.add_argument("--projeto", default="mandato-aberto-dados", help="Seu Billing Project ID (padrão: mandato-aberto-dados)")
    
    args = parser.parse_args()
    
    # Executa a inspeção
    inspecionar_tabela(args.tabela, args.projeto)