from functools import lru_cache

from fastapi import Depends

from app.repositories.transaction_repository import get_transaction_repository
from app.repositories.zip_repository import get_zip_repository
from app.repositories.interfaces import ITransactionRepository, IZipRepository

from app.schemas.transactions import Transaction, TransactionCreate


class TransactionService:
    """Сервис обработки транзакций."""

    def __init__(self, zip_repo: IZipRepository, transaction_repo: ITransactionRepository) -> None:
        self._zip_repo = zip_repo
        self._transaction_repo = transaction_repo

    async def create_transaction(self, obj_in: TransactionCreate) -> None:
        await self._transaction_repo.create(obj_in=obj_in)

    async def bulk_create_transactions(self, objs_in: list[TransactionCreate]) -> None:
        ...

    async def get_transaction(self, obj_id: str) -> Transaction:
        return await self._transaction_repo.get(obj_id=obj_id)


@lru_cache()
def get_transaction_service(
        zip_repo: IZipRepository = Depends(get_zip_repository),
        transaction_repo: ITransactionRepository = Depends(get_transaction_repository)
) -> TransactionService:
    return TransactionService(
        zip_repo=zip_repo,
        transaction_repo=transaction_repo,
    )
