import logging
import os
import aiofiles

from functools import lru_cache
from gzip import GzipFile, BadGzipFile

from app.repositories.interfaces import IArchiveRepository
from app.repositories.file_management_mixin import FileManagementMixin
from app.exceptions.gz_exceptions import GzZipError


class GzZipRepository(IArchiveRepository, FileManagementMixin):
    tmp_prefix = "unzip_"

    async def unzip(self, zip_path: str, extract_to: str | None = None) -> str:
        """Распаковка архива"""
        extract_to = await self.generate_tmp_path(extract_to)

        if not os.path.exists(zip_path):
            raise GzZipError(f"Файл {zip_path} не найден")

        try:
            with GzipFile(zip_path, 'rb') as gz_file:
                file_name = os.path.basename(zip_path).replace('.gz', '')
                output_path = os.path.join(extract_to, file_name)

                async with aiofiles.open(output_path, 'wb') as out_file:
                    content = gz_file.read()
                    await out_file.write(content)

                logging.info(f"Файл распакован: {output_path}")
                return extract_to

        except BadGzipFile:
            logging.error(f"Ошибка при распаковке файла {zip_path}")
            raise GzZipError(f"Ошибка при распаковке файла {zip_path}")

        except Exception as e:
            logging.error(f"Неизвестная ошибка при распаковке файла {zip_path}: {e}")
            raise GzZipError(f"Неизвестная ошибка при распаковке файла {zip_path}: {e}")

    async def get_extracted_files(self, extract_to: str) -> list[str]:
        """Получение распакованных файлов"""
        extracted_files = []
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                extracted_files.append(os.path.join(root, file))
        return extracted_files


@lru_cache()
def get_gz_repository() -> IArchiveRepository:
    return GzZipRepository()
