import os
import sys

from aiohttp import abc
from decouple import config
from loguru import logger


class AccessLogger(abc.AbstractAccessLogger):
    def log(self, request, response, time):
        logger.info(
            "{} {} {} done in {:.5f}s: {}",
            request.remote,
            request.method,
            request.path,
            time,
            response.status,
        )


def setup_logger() -> None:
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(
        os.environ.get(
            "LOGGER_PATH", default=config("LOGGER_PATH", default="gif_api.log")
        ),
        level="INFO",
    )
