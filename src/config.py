from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Production-ready Fallback Engine Setup
    DATABASE_URL: str = "sqlite:///business.db"
    
    # Global Security Baselines
    SECRET_KEY: str = "b1z0s_g10b41_m3g4_saas_p14tf0rm_s3cr3t_k3y_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Extended SaaS Dynamic Core Parameters
    REDIS_URL: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASS: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
