from logging.config import fileConfig
import os
import sys
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

# Add the parent directory to sys.path so we can import our app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import our models
from app.database import Base
# Import all models so they're registered with SQLAlchemy
from app.models import User

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Load environment variables
load_dotenv()

# Get database connection parameters
db_user = os.getenv("DB_USER", "kevinlin192003")
db_pass = os.getenv("DB_PASS", "@Kevinlin1234")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "fastapi_app")

# URL encode the password
encoded_pass = quote_plus(db_pass)
url = f"postgresql://{db_user}:{encoded_pass}@{db_host}/{db_name}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
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
    # This is the key part - instead of using engine_from_config, 
    # we create the engine manually with our URL
    connectable = create_engine(url)

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
