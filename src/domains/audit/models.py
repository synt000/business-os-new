from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import TenantModel


class AuditLog(TenantModel):
    __tablename__ = "audit_logs"

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    table_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    record_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    changes: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )


