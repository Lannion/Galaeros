import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from core.config import settings
from models.base import Base
# Import all model modules here so they register on Base.metadata, e.g.:
# from models import user, listing, booking  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override the sqlalchemy.url from alembic.ini with our real settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Tables owned by Postgres extensions (postgis, postgis_tiger_geocoder,
# postgis_topology, pointcloud, mobilitydb, ...) that may already exist in
# the target database but are NOT part of our application's model graph.
# Without this filter, Alembic's autogenerate diffs the live DB against
# our metadata and concludes these should be dropped, since they aren't
# declared as SQLAlchemy models.
EXTENSION_OWNED_TABLES = {
    "spatial_ref_sys",  # postgis core
    "county", "us_gaz", "zip_lookup_base", "pagc_lex", "addr",
    "geocode_settings", "loader_platform", "state", "edges",
    "state_lookup", "pagc_gaz", "tabblock20", "county_lookup",
    "featnames", "place_lookup", "loader_variables", "layer",
    "secondary_unit_lookup", "loader_lookuptables",
    "geocode_settings_default", "pagc_rules", "direction_lookup",
    "tabblock", "us_rules", "place", "zcta5", "cousub",
    "street_type_lookup", "bg", "zip_state", "zip_lookup_all",
    "mobilitydb_opcache", "faces", "addrfeat", "zip_lookup",
    "topology", "pointcloud_formats", "zip_state_loc",
    "countysub_lookup", "us_lex", "tract",
}


def include_object(object, name, type_, reflected, compare_to):
    """Exclude extension-owned tables (and their indexes) from autogenerate diffs."""
    if type_ == "table" and name in EXTENSION_OWNED_TABLES:
        return False
    if type_ == "index" and object.table.name in EXTENSION_OWNED_TABLES:
        return False
    return True


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
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()