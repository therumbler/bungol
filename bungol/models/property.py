from dataclasses import dataclass
import logging
from typing import Optional, List


logger = logging.getLogger(__name__)


@dataclass
class BungolProperty:
    """A Bungol Property"""

    price_changes: List[dict]
    saved: Optional[bool]
    blocked: Optional[bool]
    info: dict
    display_marketing: bool

    @property
    def image_urls(self) -> list:
        """returns a list of URL strings"""
        mls = self.info["mls_number"]
        template = "https://static.bungol.ca/treb/{mls}/{mls}-{num}.jpg"
        photo_count = self.info["photo_count"]
        return [
            u
            for u in [
                template.format(mls=mls, num=num) for num in range(1, photo_count + 1)
            ]
        ]

    def _image_html_list(self):
        list = [f'<img src="{u}" />' for u in self.image_urls]
        if not list:
            logger.error("no images")
        return list

    def to_html(self):
        """this is a bit silly, but I'm using an f-string to create HMTL."""
        sold_price = "N/A"
        if self.info["sold_price"]:
            sold_price = f"${self.info['sold_price']:,}"

        list_price = f"${self.info['list_price']:,}"
        return f"""<div class="property">
        <h2>{self.info['street']} {self.info["city"]}</h2>
        
        <h3 class="client-remarks">{self.info["client_remarks"]}</h3>
        <h4>List Price: {list_price}</h4>
        <h4>Sold Price: {sold_price}</h4>
        
        <div class="images">
        {' '.join(self._image_html_list())}
        </div>
        </div>
        """
