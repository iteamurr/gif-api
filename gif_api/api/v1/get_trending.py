from __future__ import annotations

import datetime

import pydantic
from aiohttp import web

from gif_api import config, dto
from gif_api.api import api_v1
from gif_api.db.utils import trending as trending_utils


class Request(api_v1.BaseRequest):
    trending_date: datetime.date

    @pydantic.validator("trending_date", pre=True)
    def parse_trending_date(cls, value):
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()


async def handler(request: Request, settings: config.Settings) -> web.Response:
    async with settings.get_session() as session:
        trendings = await trending_utils.get_trendings_by_date(
            request.trending_date, session
        )
    return web.json_response(to_response(trendings), status=200)


def to_response(trendings: list[dto.Gif]) -> dict:
    return {
        "trendings": [
            {
                "gif_id": str(gif.gif_id),
                "title": gif.title,
                "url": gif.url,
                "rating": gif.rating,
            }
            for gif in trendings
        ]
    }
