from functools import cached_property
from json import JSONDecodeError

from fake_useragent import UserAgent
from httpx import AsyncClient

from .base import AbstractTool

ua = UserAgent(min_percentage=0.5)


class Browser(AbstractTool):
    "fetch an url. the only paremeter `url`"

    name = "fetch"

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = AsyncClient(http2=True, headers={"accept": "application/json,text/html,text/*"})
        return self._client

    @property
    def headers(self):
        return {"user-agent": ua.random}

    async def __call__(self, url: str):
        res = await self.client.get(url, headers=self.headers)
        try:
            return res.json()
        except JSONDecodeError:
            return res.text
