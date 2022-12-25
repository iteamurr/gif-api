from aiohttp import web

from gif_api import config


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
