# 3. Specific Implementations
import json
from typing import List

import yt_dlp

from ...types.PlatformHandler import PlatformHandler


class Youtube(PlatformHandler):
    def __init__(self):
        self.outlets = ["history"]

    def get_history_titles(self) -> List[str]:
        titles = []
        url = "https://www.youtube.com/feed/history"

        # breakpoint()
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

            with open("output.json", "w") as f:
                f.truncate(0)  # Erase file contents first
                json.dump(
                    ydl.sanitize_info(info), f, indent=4, sort_keys=True
                )  # Pretty-print JSON with indentation and sorted keys
            entries = info.get("entries", [])

            for entry in entries:
                if entry:
                    title = entry.get("title", "N/A")
                    print(title)  # Add printing to match CLI
                    titles.append(title)

        return titles

    def update(self):
        """
        Fetches all of the videos in a playlist specified in the config
        and updates the database accordingly.
        """
        # Example: get titles from history and update a database
        titles = self.get_history_titles()
        print("hello")

        # Here you would connect to your database and insert/update records
        # For demonstration, just print them:
        for idx, title in enumerate(titles, start=1):
            print(f"Video {idx}: {title}")
            # e.g. cursor.execute("INSERT INTO videos (title) VALUES (?)", (title,))

        # print(f"Updated database with {len(titles)} videos.")
