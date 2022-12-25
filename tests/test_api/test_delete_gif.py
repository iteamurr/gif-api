import uuid

import pytest
from sqlalchemy import future, orm

from gif_api.db import models


async def test_delete_gif(api_client, session, test_gif):
    response = await api_client.delete(f"/api/v1/gif/{test_gif.gif_id}")
    assert response.status == 204

    statement = future.select(models.Gif).where(models.Gif.gif_id == test_gif.gif_id)
    gif = (await session.execute(statement)).scalar_one_or_none()

    assert gif is None


@pytest.mark.parametrize("data", [{"trending_date": "2022-12-21"}])
async def test_delete_gif_with_trending(api_client, session, test_gif, data):
    data.update({"gif_id": str(test_gif.gif_id)})

    response = await api_client.post("/api/v1/trending", json=data)
    assert response.status == 200

    response = await api_client.delete(f"/api/v1/gif/{test_gif.gif_id}")
    assert response.status == 204

    statement = future.select(models.Gif).where(models.Gif.gif_id == test_gif.gif_id)
    gif = (await session.execute(statement)).scalar_one_or_none()

    statement = (
        future.select(models.Trending)
        .where(
            models.Trending.gif_id == data["gif_id"]
            and models.Trending.trending_date == data["trending_date"]
        )
        .options(orm.selectinload(models.Trending.trending_gif))
    )
    trending = (await session.execute(statement)).scalar_one_or_none()

    assert trending is None
    assert gif is None


async def test_delete_gif_without_gif_in_db(api_client):
    response = await api_client.delete(f"/api/v1/gif/{uuid.uuid4()}")
    assert response.status == 404
