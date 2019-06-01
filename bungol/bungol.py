"""Python asyncio interface to bungol.ca"""
import json
import logging
import re
from typing import Optional

import aiohttp

from .models import BungolProperty

logger = logging.getLogger(__name__)


class Bungol:
    HEADERS = {"X-Requested-With": "XMLHttpRequest"}

    def __init__(self, *args, **kwargs):
        self.var = "hi"

        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers=self.HEADERS
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.close()

    async def search(self, value: str) -> dict:
        url = "https://www.bungol.ca/api/property-search-autocomplete/"
        params = {"value": value}
        async with self.session.get(url, params=params) as resp:
            return await resp.json()

    @staticmethod
    def _html_to_property(html: str) -> Optional[BungolProperty]:
        pattern = r"let property = (.*\}?);"
        match = re.search(pattern, html)
        if not match:
            logger.error("no match")
            return None
        json_str = match.group(1)
        obj = json.loads(json_str)
        return BungolProperty(**obj)

    async def get_property(
        self, mls_number: str, listing_id: int
    ) -> Optional[BungolProperty]:
        """get the property dict"""
        full_slug = f"PLACEHOLDER-{mls_number}-{listing_id}"
        url = f"https://www.bungol.ca/listing/{full_slug}"
        async with self.session.get(url) as resp:
            html = await resp.text()
            property_ = self._html_to_property(html)
        return property_
