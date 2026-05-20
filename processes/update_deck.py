from processes.DatabaseManager import DatabaseManager
from custom_types.Note import Note
from util.config import config_get
from util.getters import get_platform_handler_by_name


def update_deck():
    platforms: list[str] = config_get("platforms") or []

    notes: list[Note] = []
    for platform_name in platforms:
        platform = get_platform_handler_by_name(platform_name)
        if platform is None:
            print(f"Platform {platform_name} not found, skipping.")
            return

        notes.extend(platform.update())

    # TODO: perform bulk, atomic update
    for note in notes:
        # WARN: I don't feel safe having this be two seperate calls

        DatabaseManager.add_note(note)
