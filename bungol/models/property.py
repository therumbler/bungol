from typing import Optional, List
from dataclasses import dataclass


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
        return [f'<img src="{u}" />' for u in self.image_urls]

    def to_html(self):
        """this is a bit silly, but I'm using an f-string to create HMTL."""
        return f"""<div class="property">
        <h2>{self.info['street']} {self.info["city"]}</h2>
        
        <h3 class="client-remarks">{self.info["client_remarks"]}</h3>
        <h3>Sold Price: ${self.info["sold_price"]:,}</h3>
        <div class="images">
        {' '.join(self._image_html_list())}
        </div>
        </div>
        """
