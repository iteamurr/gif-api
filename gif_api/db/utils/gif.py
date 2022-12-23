import uuid

from sqlalchemy import engine, future
from sqlalchemy.ext import asyncio as async_orm

from gif_api import dto
from gif_api.db import models


async def get_gif_by_url(url: str, session: async_orm.AsyncSession) -> dto.Gif | None:
    statement = future.select(models.Gif).where(models.Gif.url == url)
    result: engine.CursorResult = await session.execute(statement)
    db_gif = result.scalar_one_or_none()

    gif = dto.Gif.from_model(db_gif) if db_gif is not None else None
    return gif


async def get_gif_by_gif_id(
    gif_id: uuid.UUID, session: async_orm.AsyncSession
) -> dto.Gif | None:
    statement = future.select(models.Gif).where(models.Gif.gif_id == gif_id)
    result: engine.CursorResult = await session.execute(statement)
    db_gif = result.scalar_one_or_none()

    gif = dto.Gif.from_model(db_gif) if db_gif is not None else None
    return gif


async def create_gif(gif: dto.Gif, session: async_orm.AsyncSession) -> dto.Gif:
    new_gif = models.Gif(title=gif.title, url=gif.url, rating=gif.rating)
    session.add(new_gif)
    await session.commit()
    await session.refresh(new_gif)

    gif = dto.Gif.from_model(new_gif)
    return gif
