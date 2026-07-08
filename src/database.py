import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./app.db"

# Hardened Engine Context Configuration
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Unified Database Session Injector Dependency for FastAPI routers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
