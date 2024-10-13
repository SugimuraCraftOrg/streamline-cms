from datetime import datetime
from functools import lru_cache
from typing import Dict
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    """Load project settings from environ."""

    env: str
    test: bool = False

    class Config:
        env_prefix = "project_"


@lru_cache()
def get_project_settings():
    return ProjectSettings()


class AppSettings(BaseSettings):
    """Load app settings from environ."""

    secret_key: str
    token_expire_hours: int
    timezone_name: str
    cors_origins: list

    class Config:
        env_prefix = "app_"


@lru_cache()
def get_app_settings():
    return AppSettings()


class DBSettings(BaseSettings):
    """Load DB settings from environ."""

    host: str
    port: int
    database: str
    user: str
    password: str

    @property
    def database_uri(self):
        project_settings = get_project_settings()
        if project_settings.test:
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}_test"
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def echo(self):
        project_settings = get_project_settings()
        return project_settings.env != "prod"

    @property
    def engine_info(self) -> Dict:
        info = {
            "url": self.database_uri,
            "echo": self.echo,
        }
        return info

    class Config:
        env_prefix = "db_"


@lru_cache()
def get_db_settings():
    return DBSettings()


def utc_timezone():
    return ZoneInfo("UTC")


def local_timezone():
    app_settings = AppSettings()
    return ZoneInfo(app_settings.timezone_name)


def utc_now():
    return datetime.now(utc_timezone())


def local_now():
    return datetime.now(local_timezone())
