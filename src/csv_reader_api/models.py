from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Classe base para nossos modelos SQLAlchemy
class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items" # Nome da tabela do banco de dados

    # Colunas da tabela
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(index=True)
    descricao: Mapped[str] = mapped_column()
    valor: Mapped[float] = mapped_column()