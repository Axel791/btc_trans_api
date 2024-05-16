from functools import lru_cache

from fastapi import Depends

from app.db.connection import DBConnection
from app.db.connection_fatcory import get_db_connection
from app.db.queries.neo4j.transaction_queries import (
    CREATE_TRANSACTION,
    BULK_CREATE_TRANSACTIONS,
    GET_TRANSACTION,
    GET_TRANSACTIONS_BY_BLOCK_ID
)
from app.repositories.interfaces import ITransactionRepository
from app.schemas.transactions import Transaction, TransactionCreate


class TransactionRepository(ITransactionRepository):

    def __init__(self, connection: DBConnection) -> None:
        self._connection = connection

    async def get(self, transaction_hash: str) -> Transaction | None:
        async with self._connection.session() as session:
            result = await session.run(GET_TRANSACTION, hash=transaction_hash)
            record = await result.single()
            if record:
                return Transaction(**dict(record["t"].items()))
            return None

    async def bulk_create(self, objs_in: list[TransactionCreate], batch_size: int) -> None:
        for i in range(0, len(objs_in), batch_size):
            batch = objs_in[i:i + batch_size]
            async with self._connection.session() as session:
                await session.run(BULK_CREATE_TRANSACTIONS, transactions=[obj.dict() for obj in batch])

    async def list(self, block_id: int) -> list[Transaction]:
        async with self._connection.session() as session:
            result = await session.run(GET_TRANSACTIONS_BY_BLOCK_ID, block_id=block_id)
            records = await result.single()
            if records:
                return [Transaction(**dict(record["t"].items())) for record in records]
            return []

    async def create(self, obj_in: TransactionCreate) -> Transaction:
        async with self._connection.session() as session:
            result = await session.run(CREATE_TRANSACTION, **obj_in.dict())
            record = await result.single()
            return Transaction(**dict(record["t"].items()))

@lru_cache()
def get_transaction_repository(
        db_connection: DBConnection = Depends(get_db_connection)
) -> ITransactionRepository:
    return TransactionRepository(connection=db_connection)
