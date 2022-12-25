from __future__ import annotations

import datetime
import uuid

import pydantic
from aiohttp import web

from gif_api import config, dto
from gif_api.api import api_v1
from gif_api.db.utils import gif as gif_utils
from gif_api.db.utils import trending as trending_utils


class Request(api_v1.BaseRequest):
    gif_id: uuid.UUID
    trending_date: datetime.date

    @pydantic.validator("trending_date", pre=True)
    def parse_trending_date(cls, value):
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()


async def handler(request: Request, settings: config.Settings) -> web.Response:
    """
    Add a GIF to trends.
    ---
    summary: Add trends.
    description: Add a GIF to trends.
    tags:
      - Trending
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/AddTrendingGifRequest"
    responses:
      "200":
        description: GIF successfully added.
      "404":
        description: The particular GIF you are requesting was not found.
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Error"
            example:
              message: The particular GIF you are requesting was not found.
              code: 404
    """
    gif = dto.Gif.from_request(request)
    async with settings.get_session() as session:
        db_gif = await gif_utils.get_gif_by_gif_id(gif.gif_id, session)
        gif_does_not_exist = db_gif is None
        if gif_does_not_exist:
            error = api_v1.Error.NOT_FOUND
            return web.json_response(data=error.response, status=error.status)

        trending_gif = await trending_utils.get_gif_trending_by_date(
            gif, gif.trending_date, session
        )
        trending_does_not_exist = trending_gif is None
        if trending_does_not_exist:
            await trending_utils.create_trending(gif, gif.trending_date, session)
    return web.Response(status=200)
