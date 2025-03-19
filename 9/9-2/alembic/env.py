import os  # Added os import to extract our variables from the environment
import sys  # Added import of sys module for working with paths
# (sys is needed for further imports,
# otherwise alembic will not see our app folder)

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Here we added our app folder to the path so that alembic could see it.
# The order of imports is intentionally broken,
# because the code is executed line by line
sys.path.append(os.path.join(sys.path[0], 'app'))

from app.core.config import settings  # Added import of our config # noqa: E402
from app.db.database import Base  # Added import of our meta-DB # noqa: E402
from app.db.models import ToDo  # noqa: E402, F401
# Added import of model so it is initialized, but it is not used
# without this import alembic may not see
# our models and will create an empty migration


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Added work with config sections / work with environment variables
# so that they become available in alembic.ini
section = config.config_ini_section
config.set_section_option(section, "DB_HOST", settings.DB_HOST)
config.set_section_option(section, "DB_PORT", settings.DB_PORT)
config.set_section_option(section, "DB_USER", settings.DB_USER)
config.set_section_option(section, "DB_NAME", settings.DB_NAME)
config.set_section_option(section, "DB_PASS", settings.DB_PASS)

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
