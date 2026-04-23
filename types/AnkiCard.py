from typing import Tuple

from .AnkiCardModel import AnkiCardModel


class AnkiCard(AnkiCardModel):
    def __init__(
        self,
        anki_card_model: AnkiCardModel,
        front: str,
        back: str,
        markers: list[Tuple[str, str]],
        score: int,
    ):
        self.title = anki_card_model.title
        self.url = anki_card_model.url
        self.thumbnail = anki_card_model.thumbnail
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
        return f"AnkiCard({', '.join(attrs)})"
