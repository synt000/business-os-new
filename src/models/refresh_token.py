from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.core.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, nullable=False, index=True)
    tenant_id = Column(String, nullable=False, index=True)

    jti = Column(String, unique=True, nullable=False, index=True)

    expires_at = Column(DateTime, nullable=False)

    revoked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
