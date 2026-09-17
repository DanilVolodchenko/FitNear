from enum import Enum
from typing import Any


def get_enum_values(enum_class: type[Enum]) -> list[Any]:
    """
    Args:
        enum_class: The Enum|StrEnum object whose values should be extracted.
    Returns:
        A list of Enum values.

    Used in SQLAlchemy enum fields, so that Alembic creates enum values correctly.
    Without it, Alembic uses the enum member names instead of their values.

    Example:
        class Table(Base):
            field: mapped_column(
                sa.Enum(
                    MyEnumObj,
                    name='<table_name>_<field_name>_enum',
                    values_callable=get_enum_values
                    )
                )
    """

    return [member.value for member in enum_class]
