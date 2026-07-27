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
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(
            User.email == email
        ).first()


    @staticmethod
    def get_all_by_tenant(db: Session, tenant_id):
        return db.query(User).filter(
            User.tenant_id == tenant_id
        ).all()


    @staticmethod
    def email_exists(db: Session, email: str) -> bool:
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
            is not None
        )
