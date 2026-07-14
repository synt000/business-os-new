from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
)

from sqlalchemy.orm import relationship

from src.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    description = Column(String)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    code = Column(
        String,
        unique=True,
        nullable=False
    )

    module = Column(String)

    description = Column(String)


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE")
    )

    permission_id = Column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE")
    )

    role = relationship("Role")

    permission = relationship("Permission")


class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    permission_id = Column(
        Integer,
        ForeignKey(
            "permissions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    is_allowed = Column(
        Integer,
        default=1
    )


    permission = relationship(
        "Permission"
    )


