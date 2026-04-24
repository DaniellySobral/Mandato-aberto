from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o SQLite
# Esta configuração fará com que eu crie um arquivo chamado 'mandato_aberto.db' na pasta raiz do meu projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./mandato_aberto.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Esta é a função que eu vou usar sempre que precisar acessar o banco de dados nas outras partes do meu código
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()