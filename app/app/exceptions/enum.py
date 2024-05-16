from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return str(self.name) == str(getattr(other, "name", other))


class ErrorEnum(StrEnum):
    UNEXPECTED_ERROR = "Произошла неизвестная ошибка ошибка."


class GzZIPErrorEnum(StrEnum):
    BAD_GZ_ZIP_FILE_ERROR = "Ошибка при разархивации файла {}"
