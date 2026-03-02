from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes import router

app = FastAPI(title="Mandato Aberto API")

# Cria as tabelas caso não existam
Base.metadata.create_all(bind=engine)

# Inclui as rotas que definimos em routes.py
app.include_router(router)

@app.get("/")
def home():
    return {"mensagem": "Bem-vinda à API Mandato Aberto! Acesse /docs para testar os filtros."}