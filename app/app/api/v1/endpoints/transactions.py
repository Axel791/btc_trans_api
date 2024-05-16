from fastapi import APIRouter, Depends, status, UploadFile, File

from app.core.logger import SafeLoggingRoute
from app.schemas.transactions import TransactionCreate, Transaction
from app.services.transaction_service import TransactionService, get_transaction_service
from app.api.pagination import PaginationParams, Paginator, BasePaginationResponse

router = APIRouter()


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
) -> Transaction | None:
    return await transaction_service.get_transaction(transaction_hash=transaction_hash)


@router.post(
    "/create",
    summary="Create transaction",
    status_code=status.HTTP_200_OK,
    description="Create transaction",
    response_model=Transaction,
)
async def create_transaction(
        transaction: TransactionCreate,
        transaction_service: TransactionService = Depends(get_transaction_service)
) -> Transaction:
    return await transaction_service.create_transaction(obj_in=transaction)


@router.post(
    "/bulk",
    summary="Bulk create transactions",
    status_code=status.HTTP_200_OK,
    description="Bulk create transactions from Blockchair dump",
)
async def bulk_create_transaction(
    batch_size: int = 100,
    file: UploadFile = File(...),
    transaction_service: TransactionService = Depends(get_transaction_service)
) -> None:
    await transaction_service.bulk_create_transactions_from_file(file=file, batch_size=batch_size)


@router.get(
    "/list",
    summary="List transaction",
    status_code=status.HTTP_200_OK,
    description="List transactions by block_id",
)
async def list_transactions(
    block_id: int,
    transaction_service: TransactionService = Depends(get_transaction_service),
    pagination: PaginationParams = Depends(PaginationParams)
) -> BasePaginationResponse[Transaction]:
    response = await transaction_service.get_list_transactions(block_id=block_id)
    paginator = Paginator(data=response, pagination_params=pagination)
    return paginator.get_response()
