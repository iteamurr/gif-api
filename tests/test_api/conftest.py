import random
import uuid

import pytest

from gif_api.db import models


def random_gif():
    gif_uuid = str(uuid.uuid4())
    gif = {
        "title": f"New {gif_uuid} gif",
        "url": f"http://{gif_uuid}.ru",
        "rating": random.choice(list(models.GifRating)),
    }
    yield gif


@pytest.fixture(params=random_gif())
async def test_gif(session, request):
    gif = request.param
    new_gif = models.Gif(title=gif["title"], url=gif["url"], rating=gif["rating"])

    session.add(new_gif)
    await session.commit()
    await session.refresh(new_gif)

    return new_gif


@pytest.fixture
async def test_trendings(session):
    trendings = list()
    for gif in [next(random_gif()) for _ in range(3)]:
        new_gif = models.Gif(title=gif["title"], url=gif["url"], rating=gif["rating"])

        session.add(new_gif)
        await session.commit()
        await session.refresh(new_gif)

        trending = models.Trending(
            gif_id=new_gif.gif_id, trending_date=new_gif.create_datetime
        )
        session.add(trending)
        await session.commit()

        trendings.append(new_gif)
    return trendings
