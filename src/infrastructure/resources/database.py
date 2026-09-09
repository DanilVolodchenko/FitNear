import psycopg
from psycopg import sql
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import PostgresConfig


async def create_db_if_not_exists(psql_config: PostgresConfig) -> None:
    conn_info = f'dbname=postgres host={psql_config.host} port={psql_config.port} user={psql_config.username} password={psql_config.pwd}'

    async with await psycopg.AsyncConnection.connect(conn_info, autocommit=True) as connection:
        async with connection.cursor() as cursor:
            check_db_stmt = sql.SQL('SELECT 1 FROM pg_database WHERE datname = %s')

            await cursor.execute(check_db_stmt, (psql_config.db,))
            exists = await cursor.fetchone()

            if not exists:
                create_db_stmt = sql.SQL('CREATE DATABASE {}').format(sql.Identifier(psql_config.db))
                await cursor.execute(create_db_stmt)


def new_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        psql_config.dsn.unicode_string(),
        pool_size=15,
        max_overflow=15,
        connect_args={
            'connect_timeout': 5,
        },
    )
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
