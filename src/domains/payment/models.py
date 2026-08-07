from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import BaseModel


class PaymentMethod(BaseModel):
    __tablename__ = "payment_methods"

    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    ledger_account = Column(String, nullable=False)
    active = Column(Boolean, default=True)

    tenant_links = relationship(
        "TenantPaymentMethod",
        back_populates="payment_method",
    )


class TenantPaymentMethod(BaseModel):
    __tablename__ = "tenant_payment_methods"

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False,
    )

    payment_method_id = Column(
        String,
        ForeignKey("payment_methods.id"),
        nullable=False,
    )

    enabled = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

    payment_method = relationship(
        "PaymentMethod",
        back_populates="tenant_links",
    )
