from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_csv_setting(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


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
    cors_allow_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    cors_allow_methods: str = "GET,POST,OPTIONS"
    cors_allow_headers: str = "*"
    cors_allow_credentials: bool = True
    gzip_minimum_size: int = 200
    trusted_hosts: str = "localhost,127.0.0.1,testserver"
    security_frame_options: str = "DENY"
    security_content_type_options: str = "nosniff"
    security_referrer_policy: str = "strict-origin-when-cross-origin"
    https_redirect_enabled: bool = False
    request_max_body_size: int = 100_000
    slow_request_threshold_ms: float = 500.0
    rate_limit_window_seconds: int = 60
    rate_limit_max_requests: int = 3
    rate_limit_paths: str = "/lookup"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_allow_origins_list(self) -> list[str]:
        return parse_csv_setting(self.cors_allow_origins)

    @property
    def cors_allow_methods_list(self) -> list[str]:
        return parse_csv_setting(self.cors_allow_methods)

    @property
    def cors_allow_headers_list(self) -> list[str]:
        return parse_csv_setting(self.cors_allow_headers)

    @property
    def trusted_hosts_list(self) -> list[str]:
        return parse_csv_setting(self.trusted_hosts)

    @property
    def rate_limit_paths_list(self) -> list[str]:
        return parse_csv_setting(self.rate_limit_paths)


@lru_cache
def get_settings() -> Settings:
    return Settings()
