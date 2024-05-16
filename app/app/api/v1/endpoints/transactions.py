from fastapi import APIRouter, Depends, status

from app.core.logger import SafeLoggingRoute
from app.schemas.transactions import TransactionCreate, Transaction
from app.services.transaction_service import TransactionService, get_transaction_service


router = APIRouter(route_class=SafeLoggingRoute)


@router.get(
    "/{transaction_hash}",
    summary="Get transaction.",
    status_code=status.HTTP_200_OK,
    description="Get transaction by ID",
    response_model=Transaction,
)
async def get_transaction(
        transaction_hash: str,
        transaction_service: TransactionService = Depends(get_transaction_service)
) -> Transaction:
    return await transaction_service.get_transaction(transaction_hash=transaction_hash)


@router.post(
    "/create",
    summary="Create transaction",
    status_code=status.HTTP_200_OK,
    description="Create transaction",
)
async def create_transaction(
        transaction: TransactionCreate,
        transaction_service: TransactionService = Depends(get_transaction_service)
) -> None:
    await transaction_service.create_transaction(obj_in=transaction)


@router.post(
    "/bulk",
    summary="Bulk create transactions",
    status_code=status.HTTP_200_OK,
    description="Bulk create transactions from Blockchair dump",
)
async def bulk_create_transaction() -> None:
    ...
