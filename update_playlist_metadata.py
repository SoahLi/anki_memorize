from typing import List

import yt_dlp


def get_history_titles(limit: int = 5) -> List[str]:
    """
    Fetch video titles from YouTube watch history using cookies from Firefox.
    Returns a list of titles.
    """
    titles = []
    # The special URL for YouTube history
    url = ":ythistory"

    with yt_dlp.YoutubeDL(
        {
            "cookiesfrombrowser": ("firefox",),
            "playlistend": limit,
            "extract_flat": True,
            "verbose": True,
            "simulate": "True",
            "ignoreerrors": True,
        }
    ) as ydl:
        # extract_info returns a dict with 'entries' for playlists
        info = ydl.extract_info(url, download=False)
        if "entries" in info:
            for entry in info["entries"]:
                if entry:  # some entries may be None if unavailable
                    titles.append(entry.get("title", "N/A"))
        else:
            # Single video case (unlikely for :ythistory, but handle)
            titles.append(info.get("title", "N/A"))

    return titles


def update_playlist_metadata():
    """
    Fetches all of the videos in a playlist specified in the config
    and updates the database accordingly.
    """
    # Example: get titles from history and update a database
    titles = get_history_titles(limit=5)

    # Here you would connect to your database and insert/update records
    # For demonstration, just print them:
    for idx, title in enumerate(titles, start=1):
        print(f"Video {idx}: {title}")
        # e.g. cursor.execute("INSERT INTO videos (title) VALUES (?)", (title,))

    print(f"Updated database with {len(titles)} videos.")
