from aiohttp import web

from bungol import Bungol, BungolProperty

with open("./bungol/templates/index.html") as f:
    HTML_TEMPLATE = f.read()


async def index(request):
    kwargs = {
        "mls_number": request.match_info["mls_number"],
        "listing_id": request.match_info["listing_id"],
    }
    async with Bungol() as bungol:
        resp: BungolProperty = await bungol.get_property(**kwargs)
    if not resp:
        return web.HTTPNotFound(text="propery not found")
    content = resp.to_html()
    html = HTML_TEMPLATE.format(content=content)
    return web.Response(content_type="text/html", text=html)


def main():
    app = web.Application()
    app.add_routes([web.get("/{mls_number}-{listing_id}", index)])
    web.run_app(app)


if __name__ == "__main__":
    main()
