from aiohttp import web

from gif_api import config, utils
from gif_api.api import api_v1
from gif_api.api.v1 import add_gif, add_trending, get_trending, health


def wrap_endpoint(
    endpoint, settings: config.Settings, request_parser: api_v1.BaseRequest = None
):
    async def wrapper(request: web.Request):
        if request_parser:
            try:
                request = await request_parser.from_request(request)
            except ValueError as err:
                error = utils.Error.UNPROCESSABLE_ENTITY
                return web.json_response(data=error.response, status=error.status)
        return await endpoint(request, settings)

    return wrapper


def setup_routes(app: web.Application, settings: config.Settings) -> None:
    app.router.add_get(
        "/api/v1/ping",
        wrap_endpoint(health.ping, settings),
    )
    app.router.add_post(
        "/api/v1/gif",
        wrap_endpoint(add_gif.handler, settings, add_gif.Request),
    )
    app.router.add_post(
        "/api/v1/trending",
        wrap_endpoint(add_trending.handler, settings, add_trending.Request),
    )
    app.router.add_get(
        "/api/v1/trending",
        wrap_endpoint(get_trending.handler, settings, get_trending.Request),
    )
