from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.models.saas_core import User


MAX_FAILED_ATTEMPTS = 5
LOCK_MINUTES = 15


def check_account_locked(user: User) -> bool:

    if not user.locked_until:
        return False

    return user.locked_until > datetime.utcnow()



def register_failed_login(
    db: Session,
    user: User
):

    current_attempts = user.failed_login_attempts or 0

    user.failed_login_attempts = current_attempts + 1


    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:

        user.locked_until = (
            datetime.utcnow()
            +
            timedelta(minutes=LOCK_MINUTES)
        )

        user.failed_login_attempts = 0


    db.commit()



def register_success_login(
    db: Session,
    user: User
):

    user.failed_login_attempts = 0

    user.locked_until = None

    user.last_login_at = datetime.utcnow()

    db.commit()
