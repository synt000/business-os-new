from sqlalchemy.orm import Session

from src.models.saas_core import AIBusinessMemory


def save_ai_memory(
    db: Session,
    tenant_id: str,
    memory_type: str,
    content: str
):

    memory = AIBusinessMemory(
        tenant_id=tenant_id,
        memory_type=memory_type,
        content=content
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory



def get_ai_memory(
    db: Session,
    tenant_id: str,
    limit: int = 20
):

    return (
        db.query(AIBusinessMemory)
        .filter(
            AIBusinessMemory.tenant_id == tenant_id
        )
        .order_by(
            AIBusinessMemory.created_at.desc()
        )
        .limit(limit)
        .all()
    )
