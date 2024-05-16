from app.exceptions.base import BaseError
from app.exceptions.enum import ZIPErrorEnum


class ZipError(BaseError):

    def __init__(self, zip_file_name: str):
        super().__init__(ZIPErrorEnum.BAD_ZIP_FILE_ERROR.format(zip_file_name))
