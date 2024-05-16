import aiofiles
from datetime import datetime

from aiofiles.threadpool.binary import AsyncIndirectBufferedReader

from app.repositories.interfaces import ITsvRepository
from app.repositories.file_management_mixin import FileManagementMixin
from app.schemas.transactions import TransactionCreate


class TsvRepository(ITsvRepository, FileManagementMixin):

    async def open_tsv(self, tsv_path: str) -> AsyncIndirectBufferedReader:
        """Открытие tsv файла"""
        async with aiofiles.open(tsv_path, mode='r', encoding='utf-8') as file:
            return file

    async def parse_tsv(self, file: AsyncIndirectBufferedReader) -> list[TransactionCreate]:
        """Парсинг записей из таблицы."""
        transactions = []
        async for line in file:
            row = dict(line.strip().split('\t'))
            transaction = TransactionCreate(
                block_id=int(row['block_id']),
                hash=row['hash'],
                time=datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S'),
                size=int(row['size']),
                weight=int(row['weight']),
                version=int(row['version']),
                lock_time=int(row['lock_time']),
                is_coinbase=bool(int(row['is_coinbase'])),
                has_witness=bool(int(row['has_witness'])),
                input_count=int(row['input_count']),
                output_count=int(row['output_count']),
                input_total=int(row['input_total']),
                input_total_usd=int(row['input_total_usd']),
                output_total=int(row['output_total']),
                output_total_usd=float(row['output_total_usd']),
                fee=int(row['fee']),
                fee_usd=float(row['fee_usd']),
                fee_per_kb=float(row['fee_per_kb']),
                fee_per_kb_usd=float(row['fee_per_kb_usd']),
                fee_per_kwu=float(row['fee_per_kwu']),
                fee_per_kwu_usd=float(row['fee_per_kwu_usd']),
                cdd_total=float(row['cdd_total']),
            )
            transactions.append(transaction)
        return transactions
