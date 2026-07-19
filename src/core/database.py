import uuid

from datetime import datetime
from typing import Generator

from sqlalchemy import (
    create_engine,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    Session,
    Mapped,
    mapped_column
)

from src.core.config import settings


if settings.DATABASE_URL.lower().startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=5,
        pool_timeout=30,
        pool_recycle=300,
        pool_pre_ping=True,
        connect_args={
            "sslmode": "require"
        }
    )


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)


Base = declarative_base()


class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class BaseModel(
    Base,
    TimestampMixin
):

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


class TenantModel(
    BaseModel
):

    __abstract__ = True

    tenant_id: Mapped[str] = mapped_column(
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
