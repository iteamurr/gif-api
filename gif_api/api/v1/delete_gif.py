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
    Delete the GIF from the database.
    ---
    summary: Delete GIF.
    description: Delete the GIF from the database.
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
      "204":
        description: GIF successfully deleted.
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

        await gif_utils.delete_gif_by_gif_id(gif.gif_id, session)
    return web.Response(status=204)
