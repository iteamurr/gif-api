import argparse

from aiohttp import web

from gif_api import config, utils

parser = argparse.ArgumentParser(description="gif_api application")
parser.add_argument("--port")


def get_app() -> web.Application:
    app = web.Application()
    settings = config.Settings()

    app.on_startup.append(settings.on_startup)
    app.on_shutdown.append(settings.on_shutdown)
    utils.setup_routes(app, settings)

    return app


def main() -> None:
    utils.setup_logger()
    app = get_app()
    port = parser.parse_args().port

    web.run_app(app=app, access_log_class=utils.AccessLogger, port=port)


if __name__ == "__main__":
    main()
