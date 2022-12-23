from __future__ import annotations

import pydantic
from aiohttp import web


class BaseRequest(pydantic.BaseModel):
    @classmethod
    async def from_request(cls, request: web.Request) -> BaseRequest:
        data = await request.json()
        return cls(**data)


__all__ = ["BaseRequest"]
