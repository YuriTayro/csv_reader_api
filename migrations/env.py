from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sys
from pathlib import Path
# Calcula o caminho para a pasta raiz do projeto (onde está o pyproject.toml)
# Path(__file__).parent -> migrations
# Path(__file__).parent.parent -> pasta raiz do projeto
project_root = Path(__file__).parent.parent 

# Calcula o caminho para a pasta src dentro da raiz
src_path = project_root / 'src'

# Adiciona a pasta src ao sys.path
sys.path.append(str(src_path))

# ---- Continue com as outras importações ----
from logging.config import fileConfig
from sqlalchemy import engine_from_config
# ... etc ...
from csv_reader_api.models import Base # Esta importação agora deve funcionar
from csv_reader_api.settings import settings # E esta também

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Adicione esta parte para pegar a URL das settings
    if config.cmd_opts and config.cmd_opts.x:
      # Opção para passar argumentos extras via linha de comando (se necessário)
      pass 
    elif not context.get_x_argument(as_dictionary=True).get('url'):
      # Define a URL a partir das nossas settings se não foi passada por argumento
      config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
