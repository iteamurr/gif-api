from __future__ import annotations

import datetime

import pydantic
from aiohttp import web
from loguru import logger

from gif_api import config, dto
from gif_api.api import api_v1
from gif_api.db.utils import trending as trending_utils


class Request(api_v1.BaseRequest):
    trending_date: datetime.date

    @pydantic.validator("trending_date", pre=True)
    def parse_trending_date(cls, value):
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()


async def handler(request: web.Request, settings: config.Settings) -> web.Response:
    """
    Get trends for a specific date.
    ---
    summary: Get trends by date.
    description: Get trends for a specific date.
    tags:
      - Trending
    parameters:
      - name: date
        in: path
        required: true
        schema:
          $ref: "#/components/schemas/GetTrendingsRequest"
    responses:
      "200":
        description: Trends have been successfully received.
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/GetTrendingsResponse"
    """
    try:
        request: Request = Request(trending_date=request.match_info["date"])
    except pydantic.ValidationError as err:
        error = api_v1.Error.UNPROCESSABLE_ENTITY
        return web.json_response(data=error.response, status=error.status)

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
