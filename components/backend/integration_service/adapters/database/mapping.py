from sqlalchemy.orm import registry

from integration_service.application import entities
from . import tables

mapper = registry()

mapper.map_imperatively(entities.TaskResult, tables.integration_service)
