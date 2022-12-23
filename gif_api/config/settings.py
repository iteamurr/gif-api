from __future__ import annotations

import contextlib
import os
import typing

import attrs
from aiohttp import web
from decouple import config
from loguru import logger
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as async_orm


@attrs.define
class Settings:
    engine: async_orm.AsyncEngine | None = None
    POSTGRES_DB: str = os.environ.get(
        "POSTGRES_DB", default=config("POSTGRES_DB", default="gif_api_db")
    )
    POSTGRES_USER: str = os.environ.get(
        "POSTGRES_USER", default=config("POSTGRES_USER", default="gif_api_db_agent")
    )
    POSTGRES_PASSWORD: str = os.environ.get(
        "POSTGRES_PASSWORD", default=config("POSTGRES_PASSWORD", default="hackme")
    )
    POSTGRES_HOST: str = os.environ.get(
        "POSTGRES_HOST", default=config("POSTGRES_HOST", default="localhost")
    )
    POSTGRES_PORT: int = os.environ.get(
        "POSTGRES_PORT", default=config("POSTGRES_PORT", default=5432, cast=int)
    )

    def __new__(cls: Settings) -> Settings:
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __repr__(self) -> str:
        return f"<Settings(db='{self.POSTGRES_DB}')>"

    async def on_startup(self, app: web.Application = None):
        self.engine = async_orm.create_async_engine(self.database_uri(), echo=True)

        logger.info(
            "Connection to the database '{}' has been established.", self.POSTGRES_DB
        )

    async def on_shutdown(self, app: web.Application = None):
        if self.engine:
            await self.engine.dispose()

        logger.info(
            "Connection to the database '{}' has been shut down.", self.POSTGRES_DB
        )

    @contextlib.asynccontextmanager
    async def get_session(self) -> typing.AsyncGenerator[async_orm.AsyncSession]:
        async_session = orm.sessionmaker(
            self.engine, class_=async_orm.AsyncSession, expire_on_commit=False
        )
        try:
            async with async_session() as session:
                yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    def database_settings(self) -> dict:
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    def database_uri(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings()
        )

    def database_uri_sync(self) -> str:
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings()
        )
