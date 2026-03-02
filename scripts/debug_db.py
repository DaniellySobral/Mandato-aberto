from app.core.database import SessionLocal
from app.models.votacao import Votacao

db = SessionLocal()

try:
    # Pega as primeiras 5 linhas do banco para inspecionar
    print("🔍 Inspecionando as primeiras 5 linhas do banco de dados...")
    
    dados = db.query(Votacao).limit(5).all()
    
    if not dados:
        print("⚠️ O banco de votação está vazio!")
    else:
        for d in dados:
            print(f"Nome: {d.nome} | Data: {d.data_hora} | Voto: {d.voto}")
            
        # Vamos checar quais anos temos no banco
        print("\n📅 Checando os anos disponíveis nos dados...")
        # Truco rápido: pega todas as datas, pega o ano, e mostra os únicos
        anos = set()
        todos_dados = db.query(Votacao).all()
        for d in todos_dados:
            if d.data_hora:
                anos.add(d.data_hora.year)
        
        print(f"Anos encontrados no banco: {sorted(anos)}")

except Exception as e:
    print(f"Erro: {e}")
finally:
    db.close()