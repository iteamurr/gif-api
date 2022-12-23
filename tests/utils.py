import contextlib

from loguru import logger
from sqlalchemy_utils import create_database, drop_database


@contextlib.contextmanager
def temp_database(temp_db_uri: str) -> str:
    create_database(temp_db_uri)
    logger.info("Database for the tests has been created.")

    try:
        yield temp_db_uri
    finally:
        drop_database(temp_db_uri)
        logger.info("Database for the tests has been deleted.")
