from pydantic import BaseModel, PostgresDsn, RedisDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Inventory Analyzer Service"
    app_version: str = "1.0.0"

    # Azure App Insights
    applicationinsights_connection_string: str | None = None
    otel_experimental_resource_detectors: str | None = None

    # DB fields from .env
    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str

    @computed_field
    @property
    def asyncpg_url(self) -> str:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            path=self.postgres_db,
        ).unicode_string()

    @computed_field
    @property
    def postgres_url(self) -> str:
        return MultiHostUrl.build(
            scheme="postgres",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            path=self.postgres_db,
        ).unicode_string()

    class Config:
        env_file = ".env"


settings = Settings()
