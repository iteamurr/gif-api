import pytest
from sqlalchemy import future

from gif_api.db import models


@pytest.mark.parametrize("gif_data", [{"title": "New Gif", "url": "http://gifka.ru"}])
async def test_add_gif(api_client, session, gif_data):
    response = await api_client.post("/api/v1/gif", json=gif_data)
    assert response.status == 201

    body = await response.json()
    assert body["message"] == "Created."
    assert body["gif_id"] is not None

    statement = future.select(models.Gif).where(models.Gif.url == gif_data["url"])
    gif = (await session.execute(statement)).scalar_one_or_none()
    assert str(gif.gif_id) == body["gif_id"]
    assert gif.title == gif_data["title"]


@pytest.mark.parametrize(
    "gif_data",
    [
        pytest.param(
            {"title": "New Gif 1", "url": "http://gifka1.ru", "rating": "y"},
            id="rating: y",
        ),
        pytest.param(
            {"title": "New Gif 2", "url": "http://gifka2.ru", "rating": "g"},
            id="rating: g",
        ),
        pytest.param(
            {"title": "New Gif 3", "url": "http://gifka3.ru", "rating": "pg"},
            id="rating: pg",
        ),
        pytest.param(
            {"title": "New Gif 4", "url": "http://gifka4.ru", "rating": "pg-13"},
            id="rating: pg-13",
        ),
        pytest.param(
            {"title": "New Gif 5", "url": "http://gifka5.ru", "rating": "r"},
            id="rating: r",
        ),
    ],
)
async def test_add_gif_with_rating(api_client, session, gif_data):
    response = await api_client.post("/api/v1/gif", json=gif_data)
    assert response.status == 201

    body = await response.json()
    assert body["message"] == "Created."
    assert body["gif_id"] is not None

    statement = future.select(models.Gif).where(models.Gif.url == gif_data["url"])
    gif = (await session.execute(statement)).scalar_one_or_none()
    assert str(gif.gif_id) == body["gif_id"]
    assert gif.title == gif_data["title"]
    assert gif.rating == gif_data["rating"]


@pytest.mark.parametrize("gif_data", [{"title": "New Gif", "url": "http://gifka.ru"}])
async def test_add_dublicated_gif(api_client, gif_data):
    response = await api_client.post("/api/v1/gif", json=gif_data)
    assert response.status == 201

    response = await api_client.post("/api/v1/gif", json=gif_data)
    assert response.status == 409
