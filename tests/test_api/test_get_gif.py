import uuid

from sqlalchemy import future

from gif_api.db import models


async def test_get_gif(api_client, session, test_gif):
    response = await api_client.get(f"/api/v1/gif/{test_gif.gif_id}")
    assert response.status == 200

    body = await response.json()
    assert body["gif_id"] is not None

    statement = future.select(models.Gif).where(models.Gif.gif_id == body["gif_id"])
    gif: models.Gif = (await session.execute(statement)).scalar_one_or_none()

    assert str(gif.gif_id) == body["gif_id"]
    assert gif.title == body["title"]
    assert gif.url == body["url"]
    assert gif.rating == body["rating"]
    assert gif.create_datetime.isoformat() == body["create_datetime"]
    assert gif.update_datetime.isoformat() == body["update_datetime"]


async def test_get_gif_without_gif_in_db(api_client):
    response = await api_client.get(f"/api/v1/gif/{uuid.uuid4()}")
    assert response.status == 404
