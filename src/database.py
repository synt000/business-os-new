import os
import uuid

from datetime import datetime

from sqlalchemy import (
    create_engine,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    Mapped,
    mapped_column,
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"
)


if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False
        }
    )
else:
    engine = create_engine(
        DATABASE_URL
    )


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
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



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
