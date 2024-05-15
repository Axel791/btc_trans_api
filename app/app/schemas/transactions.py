from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    """Базовая модель транзакции"""
    block_id: int
    hash: str
    time: datetime
    size: int
    weight: int
    version: int
    lock_time: int
    is_coinbase: bool
    has_witness: bool
    input_count: int
    output_count: int
    input_total: int
    input_total_usd: int
    output_total: int
    output_total_usd: float
    fee: int
    fee_usd: float
    fee_per_kb: float
    fee_per_kb_usd: float
    fee_per_kwu: float
    fee_per_kwu_usd: float
    cdd_total: float


class TransactionCreate(TransactionBase):
    """Создание транзакции"""


class Transaction(TransactionBase):
    """Транзакция"""
    id: str

    class Config:
        orm_mode = True
