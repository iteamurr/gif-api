from aiohttp import web

from gif_api import config
from gif_api.api import api_v1
from gif_api.api.v1 import (
    add_gif,
    add_trending,
    delete_gif,
    get_gif,
    get_trending,
    health,
)


def wrap_endpoint(
    endpoint, settings: config.Settings, request_parser: api_v1.BaseRequest = None
):
    async def wrapper(request: web.Request):
        if request_parser:
            try:
                request = await request_parser.from_request(request)
            except ValueError:
                try:
                    request = await request_parser.from_path(request.match_info)
                except ValueError:
                    error = api_v1.Error.UNPROCESSABLE_ENTITY
                    return web.json_response(data=error.response, status=error.status)
        return await endpoint(request, settings)

    return wrapper


def setup_routes(app: web.Application, settings: config.Settings) -> None:
    app.router.add_get(
        "/api/v1/ping",
        wrap_endpoint(health.ping, settings),
    )
    app.router.add_get(
        "/api/v1/ping_db",
        wrap_endpoint(health.ping_db, settings),
    )
    app.router.add_get(
        "/api/v1/gif/{gif_id}",
        wrap_endpoint(get_gif.handler, settings, get_gif.Request),
    )
    app.router.add_post(
        "/api/v1/gif",
        wrap_endpoint(add_gif.handler, settings, add_gif.Request),
    )
    app.router.add_delete(
        "/api/v1/gif/{gif_id}",
        wrap_endpoint(delete_gif.handler, settings, delete_gif.Request),
    )
    app.router.add_post(
        "/api/v1/trending",
        wrap_endpoint(add_trending.handler, settings, add_trending.Request),
    )
    app.router.add_get(
        "/api/v1/trending/{trending_date}",
        wrap_endpoint(get_trending.handler, settings, get_trending.Request),
    )
