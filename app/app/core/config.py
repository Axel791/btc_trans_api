from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Settings(BaseSettings):
    """Настройки проекта"""

    api_v1_str: str = Field(title="Prefix для V1", default="/api/v1")
    debug: bool = Field(title="Режим отладки", default=True)
    log_level: LogLevel = Field(title="Уровень логирования", default=LogLevel.INFO)
    project_name: str = Field(
        title="Имя проекта", default="Unnamed", alias="PROJECT_SLUG"
    )

    db_type: str = Field(title="Тип базы данных", default="neo4j")
    db_user: str = Field(title="Пользователь БД")
    db_password: str = Field(title="Пароль БД")
    db_host: str = Field(title="Хост БД")
    db_port: int = Field(title="Порт БД", default=7687)

    @property
    def db_uri(self) -> str:
        return f"bolt://{self.db_host}:{self.db_port}"

    @field_validator("log_level", mode="before")
    @classmethod
    def lower_log_level(cls, v):
        return v.lower()

    class Config:
        env_file = ".env"


settings = Settings()
