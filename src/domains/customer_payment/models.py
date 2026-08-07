import uuid

from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.core.database import Base


class CustomerPayment(Base):
    __tablename__ = "customer_payments"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    payment_number: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    customer_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("customers.id"),
        nullable=False
    )

    receivable_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("receivables.id"),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    payment_method: Mapped[str] = mapped_column(
        String,
        default="CASH"
    )

    status: Mapped[str] = mapped_column(
        String,
        default="COMPLETED"
    )

    tenant_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("tenants.id"),
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default="now()"
    )
