import datetime

from sqlalchemy import engine, future, orm
from sqlalchemy.ext import asyncio as async_orm

from gif_api import dto
from gif_api.db import models


async def get_gif_trending_by_date(
    gif: dto.Gif, date: datetime.date, session: async_orm.AsyncSession
) -> dto.Gif | None:
    statement = future.select(models.Trending).where(
        models.Trending.gif_id == gif.gif_id and models.Trending.trending_date == date
    )
    result: engine.CursorResult = await session.execute(statement)
    trending = result.scalar_one_or_none()

    gif = dto.Gif.from_gif(gif, date) if trending is not None else None
    return gif


async def create_trending(
    gif: dto.Gif, date: datetime.date, session: async_orm.AsyncSession
) -> dto.Gif:
    trending = models.Trending(gif_id=gif.gif_id, trending_date=date)
    session.add(trending)
    await session.commit()

    gif = dto.Gif.from_gif(gif, date)
    return gif


async def get_trendings_by_date(
    date: datetime.date, session: async_orm.AsyncSession
) -> list[dto.Gif]:
    statement = (
        future.select(models.Trending)
        .where(models.Trending.trending_date == date)
        .options(orm.selectinload(models.Trending.trending_gif))
    )
    result: engine.CursorResult = await session.execute(statement)
    trendings = [trending.trending_gif for trending in result.scalars().all()]
    return trendings
