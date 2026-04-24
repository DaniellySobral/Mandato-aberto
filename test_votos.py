from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.services.deputado_service import analisa_votos_deputado

engine = create_engine("sqlite:///mandato_aberto.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

resultados = analisa_votos_deputado(db, "Silva", 2024)
import json
print(json.dumps(resultados, indent=2, default=str))
