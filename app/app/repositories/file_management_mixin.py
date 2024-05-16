import os
import shutil
import tempfile

from app.repositories.interfaces import IFileManagementMixin


class FileManagementMixin(IFileManagementMixin):
    tmp_prefix = "download_"

    async def delete_files(self, file_paths: list[str]) -> None:
        """Удаляет файлы по заданным путям."""
        for path in file_paths:
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            elif os.path.isfile(path):
                os.remove(path)

    async def generate_tmp_path(self, local_path: str | None = None) -> str:
        """Генерирует путь для временной директории, если путь не предоставлен. Использует временный каталог."""
        if local_path is None:
            return tempfile.mkdtemp(prefix=self.tmp_prefix)
        return local_path
