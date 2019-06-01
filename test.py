import asyncio

from bungol import Bungol
from bungol.models import BungolProperty


async def main():
    """let's test something"""
    async with Bungol() as bungol:
        # resp = await bungol.search(value="117 Dawes Road")
        kwargs = {"mls_number": "E4457788", "listing_id": 3837260}
        resp: BungolProperty = await bungol.get_property(**kwargs)
        print(resp.info)


if __name__ == "__main__":
    asyncio.run(main())
