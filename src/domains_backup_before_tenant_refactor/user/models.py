from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="staff"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
