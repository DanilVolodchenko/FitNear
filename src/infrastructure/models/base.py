from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.infrastructure.utils.formatter import camel_to_snake


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return f'{camel_to_snake(cls.__name__)}s'
