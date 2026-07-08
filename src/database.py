import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. ESTABLISH BASE WORKSPACE REALTIME DATABASE TARGET
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Standard Connection Pools Context
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================================================
# PRODUCTION FIXED: FULLY COMPLIANT DEPENDENCY LIFE CYCLE INJECTOR
# ==========================================================================
def get_db():
    """Generates localized dynamic database sessions and enforces strict lifecycle closures."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Hard-sealed to completely eradicate database connection pool leaks
