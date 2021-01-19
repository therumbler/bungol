#!/home/irumble/.local/share/virtualenvs/bungol-TZ6KT7hd/bin/python
from argparse import ArgumentParser
import logging
import os
import sys

from aiohttp import web

from bungol import Bungol, BungolProperty

TEMPLATES_PATH = os.getenv('BUNGOL_TEMPLATES_PATH')


logger = logging.getLogger(__name__)

with open(f"{TEMPLATES_PATH}listing.html") as f:
    LISTING_HTML_TEMPLATE = f.read()


with open(f"{TEMPLATES_PATH}index.html") as f:
    INDEX_HTML = f.read()

async def listing(request):
    kwargs = {
        "mls_number": request.match_info["mls_number"],
        "listing_id": request.match_info["listing_id"],
    }
    async with Bungol() as bungol:
        resp: BungolProperty = await bungol.get_property(**kwargs)
    if not resp:
        return web.HTTPNotFound(text="propery not found")
    content = resp.to_html()
    if resp.info["unit"]:
        title = resp.info["unit"] + '-' + resp.info["street"]
    else:
        title = resp.info["street"]
    html = LISTING_HTML_TEMPLATE.format(content=content, title=title)
    return web.Response(content_type="text/html", text=html)


async def index(request):
    logger.info('in bungol index')
    with open(f"{TEMPLATES_PATH}index.html") as f:
        html = f.read()

    return web.Response(content_type="text/html", text=html)

async def search(request):
    value = request.query['value']
    async with Bungol() as bungol:
        resp = await bungol.search(value=value)
    return web.json_response(resp)

def make_app():
    app = web.Application()
    app.add_routes([
        web.get("/{mls_number}-{listing_id}", listing),
        web.get('/search', search),
        web.get('/', index),
    ])
    return app

def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser(description='Bungol web app')
    parser.add_argument('--port', help='the HTTP port')
    args = parser.parse_args()
    port = args.port if args.port else 2021
    app = make_app()
        
    web.run_app(app, port=port, host='127.0.0.1')


if __name__ == "__main__":
    main()
