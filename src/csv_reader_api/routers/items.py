from typing import Annotated
from fastapi import APIRouter, Depends, Query # Adiciona Query
from sqlalchemy.orm import Session

from ..database import get_session
from .. import crud, schemas

router = APIRouter(prefix="/items", tags=["items"])
DbSession = Annotated[Session, Depends(get_session)]

# --- ADICIONE ESTE ENDPOINT ---
@router.get("/", response_model=schemas.ItemList) # Usa o schema ItemList para a resposta
def read_items(
    session: DbSession, # Injeta a sessão do banco
    skip: int = Query(0, ge=0, description="Número de registros a pular"), 
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros a retornar")
):
    """
    Retorna uma lista de itens do banco de dados com paginação.
    """
    items = crud.get_items(session=session, skip=skip, limit=limit)
    return {"items": items} # Retorna no formato esperado pelo schema ItemList