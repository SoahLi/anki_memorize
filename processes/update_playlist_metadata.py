# import subprocess
#
#
# def update_playlist_metadata():
#    command = 'yt-dlp --cookies-from-browser chrome --playlist-end 5 --print "%(title)s" :ythistory -v'
#    result = subprocess.run(command, shell=True, capture_output=True, text=True)
#    if result.returncode == 0:
#        output = result.stdout.strip()
#        lines = output.split("\n")
#        for line in lines:
#            print(line)
#    else:
#        print(f"Error: {result.stderr.strip()}")
import json
from typing import List

import yt_dlp


def get_history_titles(limit: int = 5) -> List[str]:
    titles = []
    url = "https://www.youtube.com/feed/history"
    limit = 5  # Explicitly set to match --playlist-end 5

    print("Hellooihsdflkjdsahj")
    # breakpoint()
    with yt_dlp.YoutubeDL(
        {
            "cookiesfrombrowser": ("firefox",),
            "playlistend": limit,
            "extract_flat": True,
            "verbose": False,  # ← Change to False
            "quiet": True,  # ← Add this to suppress output
            "no_warnings": True,  # ← Add this to suppress warnings
            "ignoreerrors": True,
        },
        "no_verbose_headers",  # pyright: ignore
    ) as ydl:
        info = ydl.extract_info(url, download=False)

        print(json.dumps(ydl.sanitize_info(info)))
        entries = info.get("entries", [])

        for entry in entries:
            if entry:
                title = entry.get("title", "N/A")
                print(title)  # Add printing to match CLI
                titles.append(title)

    return titles


def update_playlist_metadata():
    """
    Fetches all of the videos in a playlist specified in the config
    and updates the database accordingly.
    """
    # Example: get titles from history and update a database
    titles = (limit=5)
    print("hello")

    # Here you would connect to your database and insert/update records
    # For demonstration, just print them:
    for idx, title in enumerate(titles, start=1):
        print(f"Video {idx}: {title}")
        # e.g. cursor.execute("INSERT INTO videos (title) VALUES (?)", (title,))

    # print(f"Updated database with {len(titles)} videos.")
