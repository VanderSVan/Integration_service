from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AsyncTransactionContext:

    def __init__(self, **kwargs):
        self.create_session = async_sessionmaker(**kwargs)
        self._session = None

    async def __aenter__(self) -> AsyncSession:
        if self._session is None:
            self._session = self.create_session()
        return self._session

    async def __aexit__(self, *exc):
        if self._session is None:
            return None

        try:
            if exc[0] is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
            self._session = None

        return False
