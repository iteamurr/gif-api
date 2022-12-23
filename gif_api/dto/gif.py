from __future__ import annotations

import datetime
import uuid

import attrs

from gif_api.api import api_v1
from gif_api.db import models


@attrs.define(frozen=True)
class Gif:
    gif_id: uuid.UUID
    title: str
    url: str
    rating: models.GifRating
    create_datetime: datetime.datetime
    update_datetime: datetime.datetime
    trending_date: datetime.date

    @classmethod
    def from_gif(cls, gif: Gif, trending_date: datetime.date = None) -> Gif:
        return attrs.evolve(gif, trending_date=trending_date)

    @classmethod
    def from_model(cls, model: models.Gif) -> Gif:
        return cls(
            gif_id=model.gif_id,
            title=model.title,
            url=model.url,
            rating=model.rating,
            create_datetime=model.create_datetime,
            update_datetime=model.update_datetime,
            trending_date=None,
        )

    @classmethod
    def from_request(cls, request: api_v1.BaseRequest) -> Gif:
        return cls(
            gif_id=getattr(request, "gif_id", None),
            title=getattr(request, "title", None),
            url=getattr(request, "url", None),
            rating=getattr(request, "rating", None),
            create_datetime=getattr(request, "create_datetime", None),
            update_datetime=getattr(request, "update_datetime", None),
            trending_date=getattr(request, "trending_date", None),
        )
