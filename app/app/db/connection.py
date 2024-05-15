from abc import abstractmethod, ABC

from neo4j import AsyncGraphDatabase
from contextlib import asynccontextmanager


class DBConnection(ABC):

    @abstractmethod
    async def close(self):
        """Закрытие сессии"""

    @abstractmethod
    @asynccontextmanager
    async def session(self):
        """Контекстный менеджер для получения сессии"""


class Neo4jConnection(DBConnection):
    """Класс для подключения к БД neo4j"""

    def __init__(self, uri, user, password) -> None:
        self._driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def close(self):
        """Закрытие сессии"""
        await self._driver.close()

    @asynccontextmanager
    async def session(self):
        """Контекстный менеджер для получения сессии"""
        async with self._driver.session() as session:
            yield session
