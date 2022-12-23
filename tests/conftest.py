import asyncio
import os

import pytest
from aiohttp import web
from loguru import logger
from sqlalchemy.ext import asyncio as async_orm

from gif_api import config, db, utils
from tests import utils as tests_utils


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> config.Settings:
    os.environ["POSTGRES_DB"] = "gif_api_test_db"
    test_settings = config.Settings()
    test_settings.POSTGRES_DB = "gif_api_test_db"
    return test_settings


@pytest.fixture(scope="session")
async def engine(settings: config.Settings) -> async_orm.AsyncEngine:
    await settings.on_startup()
    with tests_utils.temp_database(settings.database_uri_sync()):
        yield settings.engine
    await settings.on_shutdown()


@pytest.fixture
async def create_tables(engine: async_orm.AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
        logger.info("Tables have been created.")
    yield
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.drop_all)
        logger.info("Tables have been deleted.")


@pytest.fixture
async def session(settings: config.Settings):
    async with settings.get_session() as db_session:
        yield db_session


@pytest.fixture
async def api_client(create_tables, settings: config.Settings, aiohttp_client):
    app = web.Application()
    utils.setup_routes(app, settings)
    client = await aiohttp_client(app)
    try:
        yield client
    finally:
        await client.close()
