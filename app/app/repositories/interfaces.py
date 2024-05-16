from abc import abstractmethod, ABC

from aiofiles.threadpool.binary import AsyncIndirectBufferedReader

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
    async def create(self, obj_in: TransactionCreate) -> Transaction:
        """Создание транзакции"""


class IFileManagementMixin(ABC):
    """Интерфейс миксина по работе с файлами."""

    @abstractmethod
    async def delete_files(self, file_paths: list[str]) -> None:
        """Удаляет файлы по заданным путям."""

    @abstractmethod
    async def generate_tmp_path(self, local_path: str | None = None) -> str:
        """Генерирует путь для временной директории, если путь не предоставлен. Использует временный каталог."""


class IArchiveRepository(IFileManagementMixin, ABC):
    """Интерфейс репозитория по работе с архивами"""

    @abstractmethod
    async def unzip(self, zip_path: str, extract_to: str | None = None) -> str:
        """Распаковка архива"""

    @abstractmethod
    async def get_extracted_files(self, extract_to: str) -> list:
        """Получение распакованных файлов"""


class ITsvRepository(IFileManagementMixin, ABC):
    """Интерфейс для работы с TSV файлами."""

    @abstractmethod
    async def open_tsv(self, tsv_path: str) -> AsyncIndirectBufferedReader:
        """Открытие tsv файла"""

    @abstractmethod
    async def parse_tsv(self, file: AsyncIndirectBufferedReader) -> list[TransactionCreate]:
        """Парсинг записей из таблицы."""
