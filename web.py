from aiohttp import web

from bungol import Bungol, BungolProperty


async def index(request):
    kwargs = {
        "mls_number": request.match_info["mls_number"],
        "listing_id": request.match_info["listing_id"],
    }
    async with Bungol() as bungol:
        resp: BungolProperty = await bungol.get_property(**kwargs)
    if not resp:
        return web.HTTPNotFound(text="propery not found")
    html = resp.to_html()
    return web.Response(content_type="text/html", text=html)


def main():
    app = web.Application()
    app.add_routes([web.get("/{mls_number}-{listing_id}", index)])
    web.run_app(app)


if __name__ == "__main__":
    main()
