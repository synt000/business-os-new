from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from src.core.config import settings

# 1. ENFORCE PRODUCTION POOL INFRASTRUCTURE WITH SQLITE FUTURE COMPLIANCE
if settings.DATABASE_URL.lower().startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL, 
        connect_args={"check_same_thread": False},
        future=True  # 100% compliant with SQLAlchemy 2.0 unified execution structures
    )
else:
    # Hardened Distributed PostgreSQL Cloud Pool Control Parameters
    engine = create_engine(
        settings.DATABASE_URL, 
        pool_size=25, 
        max_overflow=15, 
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Generates localized dynamic database sessions compliant with standard FastAPI lifetimes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
