# also maybe should be named CardMetadata


from ..tables.PlatformItem import PlatformItem


class AnkiCardModel:
    def __repr__(self):
        attrs = []
        if hasattr(self, "title"):
            attrs.append(f"title={self.title!r}")
        # if hasattr(self, 'transcript'):
        #    attrs.append(f"transcript={self.transcript!r}")
        if hasattr(self, "url"):
            attrs.append(f"url={self.url!r}")
            # if hasattr(self, "thumbnail"):
            #    attrs.append(f"thumbnail=<bytes {len(self.thumbnail)}>")
            attrs.append(f"platform_item_id={self.platform_item_id!r}")
        return f"AnkiCard({', '.join(attrs)})"

    def __init__(
        self,
        # id: int,
        transcript: str,  # this shouldn't be optional
        # video_snippet: Optional[str],
        title: str,  # this shouldn't be optional
        url: str,  # this shouldn't be optional
        thumbnail: bytes,
        # platform_id: int = 0,
        # filters: list[Filter] = [],
    ):
        # self.id = id
        self.title = title
        self.transcript = transcript
        self.url = url
        self.thumbnail = thumbnail
        # self.video_snippet = video_snippet

        # self.platform_id = platform_id
        # self.filters = filters if filters is not None else []

    def add_database_info(self, platform_item: PlatformItem):
        self.platform_item_id = platform_item.id

    # self.filters = filters
