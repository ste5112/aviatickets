import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLSettings(BaseSettings):
    driver: str = Field(alias='postgresql_driver', default='postgresql+asyncpg')
    username: str = Field(alias='postgresql_username', default='postgres')
    password: str = Field(alias='postgresql_password', default='1111')
    host: str = Field(alias='postgresql_host', default='localhost')
    port: str = Field(alias='postgresql_port', default='5432')
    dbname: str = Field(alias='postgresql_dbname', default='')

    @property
    def postgresql_uri(self):
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class LoggingSettings(BaseSettings):
    log_level: str = Field(alias='log_level', default='INFO')
    log_text_formatter: bool = False


class AppSettings(PostgreSQLSettings, LoggingSettings):
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"), env_file_encoding='utf-8')


app_settings = AppSettings()
