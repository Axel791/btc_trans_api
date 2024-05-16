from app.exceptions.base import BaseError
from app.exceptions.enum import GzZIPErrorEnum


class GzZipError(BaseError):

    def __init__(self, zip_file_name: str):
        super().__init__(GzZIPErrorEnum.BAD_GZ_ZIP_FILE_ERROR.format(zip_file_name))
