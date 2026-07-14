from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Dictionary FastAPI"
    app_debug: bool = False

    postgres_db: str = "dictionary"
    postgres_user: str = "dictionary_user"
    postgres_password: str = "dictionary_pass"

    database_url: str = (
        "postgresql+psycopg://dictionary_user:dictionary_pass@localhost:5432/dictionary"
    )
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
