import uuid

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from src.core.database import Base


class PredictiveAnalytic(Base):
    __tablename__ = "predictive_analytics"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    tenant_id = Column(
        String(36),
        index=True,
        nullable=False
    )

    product_id = Column(
        String(36),
        nullable=False
    )

    current_stock_level = Column(
        Integer,
        nullable=False
    )

    predicted_sales_next_month = Column(
        Float,
        nullable=False
    )

    recommended_restock_qty = Column(
        Integer,
        nullable=False
    )

    confidence_score = Column(
        Float,
        default=0.95
    )

    calculated_at = Column(
        DateTime,
        default=datetime.utcnow
    )
