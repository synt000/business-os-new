import os

class Settings:
    PROJECT_NAME: str = "Business OS - မြန်မာလုပ်ငန်းသုံး စနစ်တော်ကြီး"
    API_VERSION_PREFIX: str = "/api/v4"
    
    # INDUSTRIAL DATABASE CLUSTER CONNECTIONS CONFIG
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///app.db")
    
    # CRITICAL PRODUCTION SECURITY CREDENTIALS
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECURE_HARDENED_KERNEL_SECRET_KEY_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    TRIAL_DURATION_DAYS: int = 3

    # OWASP INFRASTRUCTURE ROUTING CORES (FIXED MATRIX)
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # TELEMETRY RATE LIMIT ENFORCEMENTS SPEC
    RATE_LIMIT_PER_MINUTE: int = 100

settings = Settings()
