# Represents a social media outlet

from sqlmodel import Field, SQLModel


class Platform(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    # sources: Dict[str, Callable[[], List[str]]]  # e.g. {"history": self.scrape_history}


#    def __init__(self, name: str):
#        name = name.lower()
#        file_path = f"./outles/{name}.json"
#        try:
#            with open(file_path, "r") as f:
#                build_data = json.load(f)
#        except FileNotFoundError:
#            raise ValueError(
#                f"Outlet '{name}' not found. Please check the name and try again."
#            )
#
#        # I would like to have bear type validate the properties of data
#        self.get_required_packages(build_data["packages"])
#
#        self.sources: Dict[str, Callable[[], List[str]]] =
#
#    @abstractmethod
#    def get_required_packages(self, packages: list[str]):
#        pass
#
#    def scrape_sources(self, limit: int = 5) -> List[str]:
#        titles = []
#        url = "https://www.youtube.com/feed/history"
#        limit = 5  # Explicitly set to match --playlist-end 5
#
#        with yt_dlp.YoutubeDL(
#            {
#                "cookiesfrombrowser": ("firefox",),
#                "playlistend": limit,
#                "extract_flat": True,
#                "verbose": False,
#                "quiet": True,
#                "no_warnings": True,
#                "ignoreerrors": True,
#            },
#            "no_verbose_headers",  # pyright: ignore
#        ) as ydl:
#            info = ydl.extract_info(url, download=False)
#
#            print(json.dumps(ydl.sanitize_info(info)))
#            entries = info.get("entries", [])
#
#            for entry in entries:
#                if entry:
#                    title = entry.get("title", "N/A")
#                    print(title)  # Add printing to match CLI
#                    titles.append(title)
#
#        return titles
#
#    def update_playlist_metadata(self):
#        """
#        Fetches all of the videos in a playlist specified in the config
#        and updates the database accordingly.
#        """
#        # Example: get titles from history and update a database
#        titles = self.scrape_sources(limit=5)
#        print("hello")
#
#        # Here you would connect to your database and insert/update records
#        # For demonstration, just print them:
#        for idx, title in enumerate(titles, start=1):
#            print(f"Video {idx}: {title}")
#            # e.g. cursor.execute("INSERT INTO videos (title) VALUES (?)", (title,))
#
#        # print(f"Updated database with {len(titles)} videos.")
