from abc import abstractmethod, ABC
from app.schemas.transactions import TransactionCreate, Transaction


class ITransactionRepository(ABC):
    """Интерфейс репозитория транзакций"""

    @abstractmethod
    async def get(self, transaction_hash: str) -> Transaction:
        """Получение транзакции"""

    @abstractmethod
    async def bulk_create(self, objs_in: list[TransactionCreate], batch_size: int = 100) -> None:
        """Массовое создание транзакций"""

    @abstractmethod
    async def list(self) -> list[Transaction]:
        """Получение транзакций по адресу"""

    @abstractmethod
    async def create(self, obj_in: TransactionCreate) -> None:
        """Создание транзакции"""


class IZipRepository:

    @abstractmethod
    def generate_tmp_path(self, local_path: str | None = None) -> str:
        """Генерирует путь для временной директории, если путь не предоставлен. Использует временный каталог."""

    @abstractmethod
    def unzip(self, zip_path: str, extract_to: str | None = None) -> str:
        """Распаковка архива"""

    @abstractmethod
    def get_extracted_files(self, extract_to: str) -> list:
        """Получение распакованных файлов"""
