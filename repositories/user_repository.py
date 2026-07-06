from sqlalchemy.orm import Session
from domains.user.model import User

class UserRepository:

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(User).filter(
            User.username == username
        ).first()
