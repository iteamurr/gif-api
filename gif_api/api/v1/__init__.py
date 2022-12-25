from __future__ import annotations

import pydantic
from aiohttp import web

from .utils import Error, get_components


class BaseRequest(pydantic.BaseModel):
    @classmethod
    async def from_request(cls, request: web.Request) -> BaseRequest:
        data = await request.json()
        return cls(**data)

    @classmethod
    async def from_path(cls, match_info: web.UrlMappingMatchInfo) -> BaseRequest:
        data = match_info
        return cls(**data)


__all__ = ["BaseRequest", "Error", "get_components"]
