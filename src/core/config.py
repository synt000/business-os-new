import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Business OS - မြန်မာလုပ်ငန်းသုံး စနစ်တော်ကြီး"
    API_VERSION_PREFIX: str = "/api/v4"
    DATABASE_URL: str = Field(default="sqlite:///./business.db", validation_alias="DATABASE_URL")
    SECRET_KEY: Optional[str] = Field(default=None, validation_alias="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", validation_alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TRIAL_DURATION_DAYS: int = 3
    TOKEN_ISSUER: str = Field(default="business-os-enterprise", validation_alias="TOKEN_ISSUER")
    TOKEN_AUDIENCE: str = Field(default="business-os-enterprise-clients", validation_alias="TOKEN_AUDIENCE")
    ALLOWED_HOSTS: List[str] = Field(default=["127.0.0.1", "localhost"], validation_alias="ALLOWED_HOSTS")
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"], validation_alias="CORS_ORIGINS")
    RATE_LIMIT_PER_MINUTE: int = 100

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_production_secrets_exist(cls, value: Optional[str]) -> str:
        database_env = os.getenv("DATABASE_URL", "sqlite:///./business.db").lower()
        environment_state = os.getenv("ENVIRONMENT", "").upper()
        if not value or value.strip() == "":
            if "postgres" in database_env or "postgresql" in database_env or environment_state == "PRODUCTION":
                raise RuntimeError("CRITICAL_SECURITY_FAULT: SECRET_KEY_ENVIRONMENT_VARIABLE_IS_REQUIRED_ON_PRODUCTION")
            import os as native_os
            return native_os.urandom(32).hex()
        return value

    @field_validator("ALLOWED_HOSTS", "CORS_ORIGINS", mode="before")
    @classmethod
    def parse_string_to_list_array(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
