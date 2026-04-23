import requests
import yt_dlp

from ....types.AnkiCardModel import AnkiCardModel
from ....types.Source import BaseSource
from ....types.SourceType import SourceType


class YoutubeHistorySource(BaseSource):
    def __init__(self, outlet_type: SourceType):
        super().__init__(outlet_type)

    def scrape(self) -> list[AnkiCardModel]:
        url = "https://www.youtube.com/feed/history"

        # #breakpoint()
        with (
            yt_dlp.YoutubeDL(
                {
                    "cookiesfrombrowser": ("firefox",),
                    "playlistend": 2,  # TODO: add some kind of pagenation to keep fetching videos until we reach one that is already in the database
                    "extract_flat": False,
                    "verbose": False,  # ← Change to False
                    "quiet": True,  # ← Add this to suppress output
                    "no_warnings": True,  # ← Add this to suppress warnings
                    "ignoreerrors": True,
                    "no_verbose_headers": True,  # pyright: ignore
                    # Add these options for transcripts
                    "writesubtitles": True,
                    "writeautomaticsub": True,
                    "writeautomaticsub": True,
                    "subtitleslangs": ["en"],  # Only English subtitles
                    "subtitlesformat": "srt",  # use srt for best compatibility
                    "skip_download": True,
                }
            ) as ydl
        ):
            info = ydl.extract_info(url, download=False)
            # print(info)

            result: list[AnkiCardModel] = []
            for entry in info.get("entries", []):
                title = entry.get("title") or ""
                transcript_url = (
                    entry.get("requested_subtitles", {}).get("en", {}).get("url")
                )

                transcript: str | None = (
                    requests.get(transcript_url).text if transcript_url else None
                ) or None
                url = entry.get("webpage_url") or None
                thumbnail_url = entry.get("thumbnail")
                thumbnail: bytes | None = (
                    requests.get(thumbnail_url).content if thumbnail_url else None
                ) or None

                video_snippet = None

                if (
                    transcript is None
                    or url is None
                    or thumbnail is None
                    or title is None
                ):
                    print(f"Warning: No transcript found for video '{title}' ({url})")
                    continue
                card = AnkiCardModel(transcript, title, url, thumbnail)
                result.append(card)

            # with open("output.json", "w") as f:
            #    f.truncate(0)  # Erase file contents first
            #    json.dump(
            #        ydl.sanitize_info(info), f, indent=4, sort_keys=True
            #    )  # Pretty-print JSON with indentation and sorted keys

        return result
