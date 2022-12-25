from __future__ import annotations

import pydantic
from aiohttp import web

from gif_api import config, dto
from gif_api.api import api_v1
from gif_api.db import models
from gif_api.db.utils import gif as gif_utils


class Request(api_v1.BaseRequest):
    title: str
    url: pydantic.HttpUrl
    rating: models.GifRating | None


async def handler(request: Request, settings: config.Settings) -> web.Response:
    """
    Add a GIF to the database.
    ---
    summary: Add a GIF.
    description: Add a GIF to the database.
    tags:
      - GIF
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/AddGifRequest"
    responses:
      "201":
        description: GIF successfully added.
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AddGifResponse"
            example:
              message: Created.
              gif_id: 7bcd297f-77ec-48d8-9297-db4523e12659
      "409":
        description: This content already exists.
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Error"
            example:
              message: This content already exists.
              code: 409
    """
    gif = dto.Gif.from_request(request)
    async with settings.get_session() as session:
        gif_exists = (await gif_utils.get_gif_by_url(gif.url, session)) is not None
        if gif_exists:
            error = api_v1.Error.CONFLICT
            return web.json_response(data=error.response, status=error.status)
        new_gif = await gif_utils.create_gif(gif, session)
    return web.json_response(to_response(new_gif), status=201)


def to_response(gif: dto.Gif) -> dict:
    return {"message": "Created.", "gif_id": str(gif.gif_id)}
