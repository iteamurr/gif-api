from __future__ import annotations

import uuid

from aiohttp import web

from gif_api import config, dto
from gif_api.api import api_v1
from gif_api.db.utils import gif as gif_utils


class Request(api_v1.BaseRequest):
    gif_id: uuid.UUID


async def handler(request: Request, settings: config.Settings) -> web.Response:
    """
    Get full information about the GIF.
    ---
    summary: Get GIF info.
    description: Get full information about the GIF.
    tags:
      - GIF
    parameters:
      - name: gif_id
        in: path
        required: true
        schema:
          type: string
          example: 7bcd297f-77ec-48d8-9297-db4523e12659
    responses:
      "200":
        description: Full information about the gif has been received.
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/FullGifInfo"
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
        gif = await gif_utils.get_gif_by_gif_id(gif.gif_id, session)
        gif_does_not_exist = gif is None
        if gif_does_not_exist:
            error = api_v1.Error.NOT_FOUND
            return web.json_response(data=error.response, status=error.status)
    return web.json_response(to_response(gif), status=200)


def to_response(gif: dto.Gif) -> dict:
    return {
        "gif_id": str(gif.gif_id),
        "title": gif.title,
        "url": gif.url,
        "rating": gif.rating,
        "create_datetime": gif.create_datetime.isoformat(),
        "update_datetime": gif.update_datetime.isoformat(),
    }
