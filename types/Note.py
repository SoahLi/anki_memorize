from typing import Tuple

from .Item import Item


class Note:
    def __init__(
        self,
        anki_card_model: Item,
        front: str,
        back: str,
        markers: list[Tuple[str, str]],
        score: int,
    ):
        # these should be refs
        self.id = anki_card_model.id
        self.platform = anki_card_model.platform
        self.transcript = anki_card_model.transcript
        self.title = anki_card_model.title
        self.url = anki_card_model.url
        self.thumbnail = anki_card_model.thumbnail
        self.platform_item_id = anki_card_model.platform_item_id

        self.markers = markers
        self.front = front
        self.back = back
        self.score = score

    def __repr__(self):
        attrs = []
        attrs.append(f"title={self.title!r}")
        attrs.append(f"url={self.url!r}")
        attrs.append(f"thumbnail=<bytes {len(self.thumbnail)}>")
        attrs.append(f"front={self.front!r}")
        attrs.append(f"back={self.back!r}")
        return f"Note({', '.join(attrs)})"
