import logging
import os

from functools import lru_cache
from tempfile import mkdtemp
from zipfile import ZipFile, BadZipFile

from app.repositories.interfaces import IZipRepository
from app.exceptions.exceptions import ZipError


class ZipRepository(IZipRepository):
    tmp_prefix = "unzip_"

    def generate_tmp_path(self, local_path: str | None = None) -> str:
        """Генерирует путь для временной директории, если путь не предоставлен. Использует временный каталог."""
        if local_path is None:
            return mkdtemp(prefix=self.tmp_prefix)
        return local_path

    def unzip(self, zip_path: str, extract_to: str | None = None) -> str:
        """Распаковка архива"""
        extract_to = self.generate_tmp_path(extract_to)
        try:
            with ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
            return extract_to
        except BadZipFile as e:
            logging.exception(e)
            raise ZipError(zip_path)

    def get_extracted_files(self, extract_to: str) -> list:
        """Получение распакованных файлов"""
        extracted_files = []
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                extracted_files.append(os.path.join(root, file))
        return extracted_files


@lru_cache()
def get_zip_repository() -> ZipRepository:
    return ZipRepository()
