from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configura o Pydantic para ler do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Variáveis de ambiente que esperamos ler
    DATABASE_URL: str = None  # URL de conexão com o banco de dados
    CSV_FILE_PATH: str = None # Caminho para o arquivo CSV

# Cria uma instância única das configurações para ser usada no projeto
settings = Settings()