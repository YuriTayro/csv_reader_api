from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# instância 'settings' que já lê o .env
from .settings import settings

# Cria a engine (conexao principal)
engine = create_engine(settings.DATABASE_URL)

# Cria objetos de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função de dependência para ser usada nos endpoints do FastAPI
def get_session()-> Session:
  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

