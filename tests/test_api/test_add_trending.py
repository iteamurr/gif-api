import uuid

import pytest
from sqlalchemy import future, orm

from gif_api.db import models


@pytest.mark.parametrize("data", [{"trending_date": "2022-12-21"}])
async def test_add_trending(api_client, session, test_gif, data):
    data.update({"gif_id": str(test_gif.gif_id)})

    response = await api_client.post("/api/v1/trending", json=data)
    assert response.status == 200

    body = await response.json()
    assert body["message"] == "Added."

    statement = (
        future.select(models.Trending)
        .where(
            models.Trending.gif_id == data["gif_id"]
            and models.Trending.trending_date == data["trending_date"]
        )
        .options(orm.selectinload(models.Trending.trending_gif))
    )
    trending = (await session.execute(statement)).scalar_one_or_none()
    assert trending is not None


@pytest.mark.parametrize("data", [{"trending_date": "2022-12-21"}])
async def test_add_trending_without_gif_in_db(api_client, data):
    data.update({"gif_id": str(uuid.uuid4())})

    response = await api_client.post("/api/v1/trending", json=data)
    assert response.status == 404

    body = await response.json()
    assert body["message"] == "The particular GIF you are requesting was not found."
