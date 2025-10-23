import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona a pasta 'src' ao sys.path para encontrar os módulos
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
sys.path.append(str(src_path))

# Agora podemos importar nossos módulos
from csv_reader_api.settings import settings
from csv_reader_api.models import Item, Base # Importamos Base também

def load_data():
    """Lê o CSV e insere os dados no banco de dados."""
    csv_path = settings.CSV_FILE_PATH
    db_url = settings.DATABASE_URL

    print(f"Lendo dados de: {csv_path}")
    print(f"Conectando ao banco de dados: {db_url}")

    try:
        # Ler o CSV com Pandas
        df = pd.read_csv(csv_path)
        print(f"CSV lido com sucesso. {len(df)} linhas encontradas.")

        # Configurar SQLAlchemy
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Garantir que a tabela exista (opcional, mas seguro)
        # Base.metadata.create_all(bind=engine) 

        db = SessionLocal()
        print("Sessão do banco de dados aberta.")

        # Limpar dados existentes (opcional, cuidado em produção!)
        num_deleted = db.query(Item).delete()
        if num_deleted > 0:
            print(f"{num_deleted} registros existentes foram deletados da tabela 'items'.")

        # Iterar sobre as linhas do DataFrame e inserir no banco
        items_adicionados = 0
        for index, row in df.iterrows():
            db_item = Item(
                id=row['ID'], # Usando o ID do CSV
                nome=row['Nome'],
                descricao=row['Descricao'],
                valor=row['Valor']
            )
            db.add(db_item)
            items_adicionados += 1

        db.commit() # Salva todas as inserções no banco
        print(f"{items_adicionados} novos itens adicionados com sucesso.")

    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado em '{csv_path}'. Verifique o caminho no .env")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        if 'db' in locals(): # Verifica se a sessão foi criada antes de tentar rollback
            db.rollback() # Desfaz qualquer mudança parcial em caso de erro
    finally:
        if 'db' in locals() and db.is_active:
            db.close() # Garante que a sessão seja fechada
            print("Sessão do banco de dados fechada.")

if __name__ == "__main__":
    print("Iniciando script de carga de dados...")
    load_data()
    print("Script de carga de dados finalizado.")