import aiohttp_swagger3 as swagger3
from aiohttp import web

import gif_api
from gif_api.api import api_v1
from gif_api.api.v1 import add_gif, add_trending, get_trending, health


def setup_swagger(app: web.Application) -> None:
    swagger_settings = swagger3.SwaggerUiSettings(path="/api/v1/docs")
    swagger_info = swagger3.SwaggerInfo(
        title="Swagger GIF API", version=gif_api.__version__
    )
    swagger = swagger3.SwaggerDocs(
        app=app,
        swagger_ui_settings=swagger_settings,
        info=swagger_info,
        components=api_v1.get_components(),
    )
    swagger.add_routes(
        [
            web.get("/api/v1/ping", health.ping),
            web.post("/api/v1/gif", add_gif.handler),
            web.post("/api/v1/trending", add_trending.handler),
            web.get("/api/v1/trending/{date}", get_trending.handler),
        ]
    )
