from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes import router

app = FastAPI(title="Mandato Aberto API")

# Aqui eu crio as tabelas no banco de dados automaticamente, caso elas ainda não existam
Base.metadata.create_all(bind=engine)

# Neste ponto, eu incluo as rotas da API que defini no arquivo routes.py
app.include_router(router)

@app.get("/")
def home():
    return {"mensagem": "Bem-vinda à API Mandato Aberto! Acesse /docs para testar os filtros."}