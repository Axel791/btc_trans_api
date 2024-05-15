from app.exceptions.enum import ErrorEnum


class BaseError(Exception):
    def __init__(self, text: str = ErrorEnum.UNEXPECTED_ERROR, errors: list[str] | None = None):
        if errors:
            self.errors = errors
        else:
            self.errors = [text]
