#!/home/irumble/.local/share/virtualenvs/bungol-TZ6KT7hd/bin/python
from argparse import ArgumentParser
import os

from aiohttp import web

from bungol import Bungol, BungolProperty

TEMPLATES_PATH = os.getenv('BUNGOL_TEMPLATES_PATH')

with open(f"{TEMPLATES_PATH}index.html") as f:
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
    html = HTML_TEMPLATE.format(content=content, title=resp.info["street_name"])
    return web.Response(content_type="text/html", text=html)


def make_app():
    app = web.Application()
    app.add_routes([web.get("/{mls_number}-{listing_id}", index)])
    return app

def main():
    parser = ArgumentParser(description='Bungol web app')
    parser.add_argument('--port', help='the HTTP port')
    args = parser.parse_args()
    port = args.port if args.port else 2021
    app = make_app()

        
    web.run_app(app, port=port)


if __name__ == "__main__":
    main()
