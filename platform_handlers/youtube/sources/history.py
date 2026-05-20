import hashlib

import requests
import yt_dlp

from custom_types.Item import Item
from custom_types.Platforms import Platforms
from custom_types.Source import BaseSource
from custom_types.SourceType import SourceType
from util.anki_getters import get_col


class YoutubeHistorySource(BaseSource):
    # I pass platform id so I can create a platform item but I can't currently because of circular imports. See the call made in add_note()
    def __init__(self, outlet_type: SourceType, platform_id: int):
        super().__init__(outlet_type, platform_id)

    def scrape(self) -> list[Item]:
        url = "https://www.youtube.com/feed/history"

        with (
            yt_dlp.YoutubeDL(
               # {
               #     "cookiesfrombrowser": ("firefox",),
               #     "playlistend": 1,  # TODO: add some kind of pagenation to keep fetching videos until we reach one that is already in the database
               #     "extract_flat": False,
               #     #"verbose": False,  # ← Change to False
               #     #"quiet": True,  # ← Add this to suppress output
               #     #"no_warnings": True,  # ← Add this to suppress warnings
               #     #"ignoreerrors": True,
               #     #"no_verbose_headers": True,  # pyright: ignore
               #     # Add these options for transcripts
               #     #"writesubtitles": True,
               #     "writeautomaticsub": True,
               #     "subtitleslangs": ["en"],  # Only English subtitles
               #     #"subtitlesformat": "srt",  # use srt for best compatibility
               #     #"skip_download": True,
               #     #"remote_components": ("ejs:github"),
               # }
            {
                "cookiesfrombrowser": ("firefox",),
                "playlistend": 1,
                "quiet": True,
                "no_warnings": True,
                "ignoreerrors": True,
                "skip_download": "True",
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en"],
            }
            ) as ydl
        ):
            # CHECK THAT YOU ARE LOGGED INTO YOUR YOUTUBE ACOUNT (and cookies )
            info = ydl.extract_info(url, download=False)

            import json

            print(json.dumps(info, indent=4, sort_keys=True))

            # print(info)

            result: list[Item] = []
            for entry in info.get("entries", []):
                title = entry.get("title") or ""
                transcript_url = (
                    entry.get("requested_subtitles", {}).get("en", {}).get("url")
                )

                # breakpoint()
                id = entry.get("id")
                col = get_col()
                if len(col.find_notes("platformItemId:" + str(id))) > 0:
                    print(f"Video '{title}' ({id}) already in database, skipping.")
                    continue

                transcript: str | None = (
                    requests.get(transcript_url).text if transcript_url else None
                ) or None

                url = entry.get("webpage_url") or None
                thumbnail_url = entry.get("thumbnail")
                thumbnail_bytes: bytes | None = (
                    requests.get(thumbnail_url).content if thumbnail_url else None
                ) or None

                final_filename: str | None = None
                if thumbnail_bytes:
                    # 1. Generate a safe filename (e.g., using hash of the URL or content)
                    #    This avoids name collisions and handles duplicates automatically.
                    file_hash = hashlib.md5(thumbnail_bytes).hexdigest()
                    # Keep the original extension if known, otherwise default to .jpg
                    # You could try to detect by looking at Content-Type header, but simple is fine.
                    filename = f"{file_hash}.jpg"

                    # 2. Get the media manager
                    media = get_col().media

                    # 3. Write the bytes directly to the media folder using write_data()
                    #    This is the most direct way when you already have bytes.
                    #    It returns the final filename (might be unchanged or modified if duplicate).
                    final_filename = media.write_data(filename, thumbnail_bytes)

                # video_snippet = None

                if (
                    transcript is None
                    or url is None
                    or final_filename is None
                    or title is None
                ):
                    print(f"Warning: No transcript found for video '{title}' ({url})")
                    continue

                item = Item(
                    id, Platforms.Youtube, transcript, title, url, final_filename
                )

                result.append(item)

            # with open("output.json", "w") as f:
            #    f.truncate(0)  # Erase file contents first
            #    json.dump(
            #        ydl.sanitize_info(info), f, indent=4, sort_keys=True
            #    )  # Pretty-print JSON with indentation and sorted keys

        return result
