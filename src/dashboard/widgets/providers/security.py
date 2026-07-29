from sqlalchemy.orm import Session

from src.security.security_query import get_security_overview


def security_widget(
    db: Session,
    user
):
    data = get_security_overview(
        db=db,
        tenant_id=user.tenant_id
    )

    return {
        "widget": "security_center",
        "title": "Security Center",
        "data": data,
    }
