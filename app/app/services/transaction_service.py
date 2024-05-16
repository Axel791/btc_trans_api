import aiofiles

from functools import lru_cache

from fastapi import Depends, UploadFile

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

    async def bulk_create_transactions_from_file(self, file: UploadFile, batch_size: int) -> None:
        tmp_path = f"/tmp/{file.filename}"
        async with aiofiles.open(tmp_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        extract_path = await self._gz_repo.unzip(tmp_path)

        tsv_file_path = await self._gz_repo.get_extracted_files(extract_path)

        tsv_file = await self._tsv_repo.open_tsv(tsv_file_path[0])

        try:
            transactions = []
            for transaction in await self._tsv_repo.parse_tsv(tsv_file):
                print(f"TRANSACTION: {transaction}")
                transactions.append(transaction)
                if len(transactions) >= batch_size:
                    await self._transaction_repo.bulk_create(transactions, batch_size=batch_size)
                    transactions = []

            if transactions:
                await self._transaction_repo.bulk_create(transactions, batch_size=batch_size)
        finally:
            await tsv_file.close()

        await self._tsv_repo.delete_files(tsv_file_path)

    async def get_transaction(self, transaction_hash: str) -> Transaction:
        return await self._transaction_repo.get(transaction_hash=transaction_hash)

    async def get_list_transactions(self, block_id: int) -> list[Transaction]:
        return await self._transaction_repo.list(block_id=block_id)


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
