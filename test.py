import asyncio
from bungol import Bungol


async def main():
    """let's test something"""
    async with Bungol() as bungol:
        # resp = await bungol.search(value="117 Dawes Road")
        kwargs = {
            "slug": "117-dawes-road-east-york",
            "mls_number": "E4457788",
            "listing_id": 3837260,
        }
        resp = await bungol.get_property(**kwargs)
        print(resp)


if __name__ == "__main__":
    asyncio.run(main())
