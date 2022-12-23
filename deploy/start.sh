#!/bin/bash

export PYTHONPATH=$(pwd)

cd gif_api/db/ && poetry run alembic upgrade head

cd ../.. && poetry run python -m gif_api --port 8000
