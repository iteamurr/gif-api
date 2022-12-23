from __future__ import annotations

import datetime
import uuid

import pydantic
from aiohttp import web

from gif_api import config, dto, utils
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
    gif = dto.Gif.from_request(request)
    async with settings.get_session() as session:
        db_gif = await gif_utils.get_gif_by_gif_id(gif.gif_id, session)
        gif_does_not_exist = db_gif is None
        if gif_does_not_exist:
            error = utils.Error.NOT_FOUND
            return web.json_response(data=error.response, status=error.status)

        trending_gif = await trending_utils.get_gif_trending_by_date(
            gif, gif.trending_date, session
        )
        trending_does_not_exist = trending_gif is None
        if trending_does_not_exist:
            await trending_utils.create_trending(gif, gif.trending_date, session)
    return web.json_response({"message": "Added."}, status=200)
