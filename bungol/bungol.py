"""Python asyncio interface to bungol.ca"""
import json
import logging
import re

import aiohttp

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
    def _html_to_property(html: str) -> dict:
        pattern = r"let property = (.*\}?);"
        match = re.search(pattern, html)
        if not match:
            logger.error("no match")
            return {}
        json_str = match.group(1)
        return json.loads(json_str)

    async def get_property(self, slug: str, mls_number: str, listing_id: int) -> dict:
        """get the property dict"""
        full_slug = f"{slug}-{mls_number}-{listing_id}"
        url = f"https://www.bungol.ca/listing/{full_slug}"
        async with self.session.get(url) as resp:
            html = await resp.text()
            property = self._html_to_property(html)
        return property
