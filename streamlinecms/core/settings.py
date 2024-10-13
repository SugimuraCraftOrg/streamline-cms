from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Dict

from pydantic_settings import BaseSettings


@lru_cache()
class ProjectSettings(BaseSettings):
    """Load project settings from environ."""

    env: str
    test: bool = False

    class Config:
        env_prefix = "project_"


@lru_cache()
class AppSettings(BaseSettings):
    """Load app settings from environ."""

    secret_key: str
    token_expire_hours: int
    timezone_offset: int

    class Config:
        env_prefix = "app_"


@lru_cache()
class DBSettings(BaseSettings):
    """Load DB settings from environ."""

    host: str
    port: int
    database: str
    user: str
    password: str

    @property
    def database_uri(self):
        project_settings = ProjectSettings()
        if project_settings.test:
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}_test"
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def echo(self):
        project_settings = ProjectSettings()
        if project_settings.env == "prod":
            return False
        return True

    @property
    def engine_info(self) -> Dict:
        info = {
            "url": self.database_uri,
            "echo": self.echo,
        }
        return info

    class Config:
        env_prefix = "db_"


def utc_timezone():
    return timezone(timedelta(hours=0))


def local_timezone():
    app_settings = AppSettings()
    return timezone(timedelta(hours=app_settings.timezone_offset))


def utc_now():
    return datetime.now(utc_timezone())


def local_now():
    return datetime.now(local_timezone())
