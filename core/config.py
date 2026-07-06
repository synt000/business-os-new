import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ==========================
    # Database
    # ==========================
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./business.db"
    )

    # ==========================
    # Email
    # ==========================
    SMTP_HOST = os.getenv(
        "SMTP_HOST",
        "smtp.gmail.com"
    )

    SMTP_PORT = int(
        os.getenv("SMTP_PORT", "587")
    )

    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")

    # ==========================
    # JWT
    # ==========================
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable is required."
        )

    ALGORITHM = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "15"
        )
    )

    REFRESH_TOKEN_EXPIRE_DAYS = int(
        os.getenv(
            "REFRESH_TOKEN_EXPIRE_DAYS",
            "7"
        )
    )


settings = Settings()
