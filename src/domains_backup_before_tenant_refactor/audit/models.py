from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database import BaseModel

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    action: Mapped[str] = mapped_column(String(100), nullable=False)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False)
    record_id: Mapped[str] = mapped_column(String(100), nullable=False)
    changes: Mapped[str] = mapped_column(Text, nullable=True)
