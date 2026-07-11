from sqlalchemy.orm import Session

from src.models.saas_core import User


class UserRepository:

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id):
        return db.query(User).filter(
            User.id == user_id
        ).first()

    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(User).filter(
            User.username == username
        ).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(
            User.email == email
        ).first()

    @staticmethod
    def username_exists(db: Session, username: str) -> bool:
        return (
            db.query(User)
            .filter(User.username == username)
            .first()
            is not None
        )

    @staticmethod
    def email_exists(db: Session, email: str) -> bool:
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
            is not None
        )
