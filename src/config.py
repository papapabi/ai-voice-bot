from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class for this application.
    Utilizes pydantic.BaseSettings for environment variables.

    These are case-insensitive by default.

    In the case where a value is specified for the same Settings field in multiple ways,
    the selected value is determined as follows (in descending order of priority):

    1. Arguments passed to the Settings class initializer.
    2. Environment variables
    3. Variables loaded from a dotenv (.env) file.
    4. Variables loaded from the secrets directory.
    5. The default field values for the Settings model.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    openai_dev_service_account: str
    openai_project_id: str
    openai_model_name: str

    api_key: str = 'foo'


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env-postgres", env_file_encoding="utf-8", extra="ignore"
    )

    postgres_dbname: str
    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=f"/{self.postgres_dbname}",
        )


class QdrantSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env-qdrant", env_file_encoding="utf-8", extra="ignore"
    )

    qdrant_host: str
    qdrant_rest_api_port: str
    qdrant_grpc_api_port: str
    openai_embedder_name: str
    openai_embedder_size: int
    collection_name: str


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_database_settings():
    return PostgresSettings()


@lru_cache()
def get_vector_database_settings():
    return QdrantSettings()


if __name__ == '__main__':
    postgres_settings = get_database_settings()
    print(f"{postgres_settings.postgres_dsn=}")