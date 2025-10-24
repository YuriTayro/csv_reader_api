from pydantic import BaseModel, ConfigDict

# Schema base para um item (sem ID, pode ser usado para criação/update se necessário)
class ItemBase(BaseModel):
    nome: str
    descricao: str
    valor: float

# Schema para retornar um item (inclui o ID e permite ler de atributos do SQLAlchemy)
# Define os campos comuns.
class ItemPublic(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True) # permite ao Pydantic ler dados diretamente de objetos SQLAlchemy

# Schema para a lista de itens (contém uma lista de ItemPublic)
class ItemList(BaseModel):
    items: list[ItemPublic]

# Schema para mensagens genéricas (usado na rota raiz)
class Message(BaseModel):
    message: str