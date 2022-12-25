from aiohttp import web

from gif_api import config
from gif_api.api import api_v1
from gif_api.db.utils import health


async def ping(request: web.Request, settings: config.Settings) -> web.Response:
    """
    Check the operation of the service.
    ---
    summary: Ping.
    description: Check the operation of the service.
    tags:
      - Health
    responses:
      "200":
        description: Pong!
        content:
          application/json:
            schema:
              properties:
                message:
                  type: string
            example:
              message: Pong!
    """
    return web.json_response({"message": "Pong!"}, status=200)


async def ping_db(request: web.Request, settings: config.Settings) -> web.Response:
    """
    Check the operation of the database.
    ---
    summary: Ping db.
    description: Check the operation of the database.
    tags:
      - Health
    responses:
      "200":
        description: Pong db!
        content:
          application/json:
            schema:
              properties:
                message:
                  type: string
            example:
              message: Pong db!
      "503":
        description: The server is temporarily unable to handle the request.
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Error"
            example:
              message: The server is temporarily unable to handle the request.
              code: 503
    """
    async with settings.get_session() as session:
        connection_status = await health.is_connection_established(session)
        connection_is_not_established = not connection_status
        if connection_is_not_established:
            error = api_v1.Error.SERVICE_UNAVAILABLE
            return web.json_response(data=error.response, status=error.status)
    return web.json_response({"message": "Pong db!"}, status=200)
