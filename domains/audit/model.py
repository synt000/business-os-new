import uuid
from sqlalchemy import Column, String, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(String, nullable=False) # Action ပြုလုပ်သူ
    action = Column(String, nullable=False) # ဥပမာ - "CREATE_PRODUCT", "LOG_MOVEMENT"
    resource_id = Column(String, nullable=True) # သက်ဆိုင်ရာ item ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
