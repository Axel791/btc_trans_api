from functools import lru_cache

from app.core.config import settings
from app.db.connection import DBConnection, Neo4jConnection


class DBConnectionFactory:
    @staticmethod
    def create_connection(db_type: str, uri: str, user: str, password: str) -> DBConnection:
        if db_type == 'neo4j':
            return Neo4jConnection(uri, user, password)
        raise ValueError(f"Unsupported database type: {db_type}")


@lru_cache()
def get_db_connection() -> DBConnection:
    return DBConnectionFactory.create_connection(
        db_type=settings.db_type,
        uri=settings.db_uri,
        user=settings.db_user,
        password=settings.db_password,
    )
