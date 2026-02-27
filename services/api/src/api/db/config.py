from api.common.utils.env import genv


def create_db_url():
    user = genv("POSTGRES_USER", "app")
    password = genv("POSTGRES_PASSWORD", "1234")
    host = genv("POSTGRES_HOST", "127.0.0.1")
    port = genv("POSTGRES_PORT", "5432")
    database = genv("POSTGRES_DB", "general")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
