from integration_service.adapters.database.utils import AsyncTransactionContext


class BaseRepository:
    def __init__(self, context: AsyncTransactionContext):
        self.context = context
