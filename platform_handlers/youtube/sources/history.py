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
        base_url: str = "https://www.youtube.com/feed/history"
        page_idx: int = 1
        
        base_opts = {
            "cookiesfrombrowser": ("firefox",),
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
        }

        result: list[Item] = []

        while True:
            opts = {
                **base_opts,
                "playlist_items": f"{page_idx}-{page_idx + self.page_size - 1}"
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(base_url, download=False)

            #breakpoint()
            entries = info.get("entries", []) if info else []
            if not entries:
                break

            for entry in info.get("entries", []):
                title = entry.get("title") or ""
                print(f"Processing video '{title}'...")
                transcript_url = (
                    entry.get("requested_subtitles", {}).get("en", {}).get("url")
                ) or None
                # breakpoint()
                id = entry.get("id") or None
                col = get_col()
                if len(col.find_notes("platformItemId:" + str(id))) > 0:
                    breakpoint()
                    print(f"Video '{title}' ({id}) already in database, skipping.")
                    break

                transcript: str | None = (
                    requests.get(transcript_url).text if transcript_url else None
                ) or None
                url = entry.get("webpage_url") or None
                thumbnail_url = entry.get("thumbnail") or None
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
            page_idx += self.page_size
            break
        return result
