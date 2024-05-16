from functools import lru_cache

from fastapi import Depends

from app.repositories.transaction_repository import get_transaction_repository
from app.repositories.gz_repository import get_gz_repository
from app.repositories.tsv_repository import get_tsv_repository
from app.repositories.interfaces import ITransactionRepository, IArchiveRepository, ITsvRepository

from app.schemas.transactions import Transaction, TransactionCreate


class TransactionService:
    """Сервис обработки транзакций."""

    def __init__(
        self,
        gz_repo: IArchiveRepository,
        tsv_repo: ITsvRepository,
        transaction_repo: ITransactionRepository
    ) -> None:
        self._gz_repo = gz_repo
        self._tsv_repo = tsv_repo
        self._transaction_repo = transaction_repo

    async def create_transaction(self, obj_in: TransactionCreate) -> Transaction:
        return await self._transaction_repo.create(obj_in=obj_in)

    async def bulk_create_transactions(self, objs_in: list[TransactionCreate]) -> None:
        ...

    async def get_transaction(self, transaction_hash: str) -> Transaction:
        return await self._transaction_repo.get(transaction_hash=transaction_hash)


@lru_cache()
def get_transaction_service(
        gz_repo: IArchiveRepository = Depends(get_gz_repository),
        tsv_repo: ITsvRepository = Depends(get_tsv_repository),
        transaction_repo: ITransactionRepository = Depends(get_transaction_repository)
) -> TransactionService:
    return TransactionService(
        gz_repo=gz_repo,
        tsv_repo=tsv_repo,
        transaction_repo=transaction_repo,
    )
