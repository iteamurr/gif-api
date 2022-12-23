from aiohttp import web

from gif_api import config


async def ping(request: web.Request, settings: config.Settings) -> web.Response:
    return web.json_response({"message": "Pong!"}, status=200)
