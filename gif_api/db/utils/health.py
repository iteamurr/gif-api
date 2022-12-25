from loguru import logger
from sqlalchemy.ext import asyncio as async_orm


async def is_connection_established(session: async_orm.AsyncSession) -> bool:
    try:
        await session.execute("SELECT 1")
    except Exception as ex:
        logger.info("A connection error occurred: {}", ex)
        return False
    else:
        return True
