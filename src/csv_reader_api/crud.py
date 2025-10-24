from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Item # Importa nosso modelo SQLAlchemy

def get_items(session: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    """Busca uma lista de itens no banco de dados com paginação."""
    items = session.scalars(
        select(Item)
        .offset(skip)
        .limit(limit)
    ).all()
    return items