from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Enum as SQLAlchemyEnum,
    Table,
)
from sqlalchemy.dialects.postgresql import JSONB

from integration_service.application.entities import TaskTypeEnum

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

integration_service = Table(
    'integration_service',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('data', JSONB, nullable=False),
    Column('task_type', SQLAlchemyEnum(TaskTypeEnum), nullable=False)
)
