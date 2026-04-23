from util.config import config_get_ensure_exists
from util.getters import get_col, get_or_create_yt_model

PLATFORM_TAG_PREFIX = "platformId_"


# NOTE: not used yet
def add_card_with_tags(platform_id: int, front: str, back: str):
    """Add card with platform_id as a tag"""
    col = get_col()
    note = col.new_note(get_or_create_yt_model())
    note["Front"] = front
    note["Back"] = back
    # note["PlatformID"] = str(platform_id)  # Still store for display

    # Add tag for fast searching
    note.tags.append(f"{PLATFORM_TAG_PREFIX}{platform_id}")

    deck_id = col.decks.id(config_get_ensure_exists("deck_name"))
    if not deck_id:
        raise Exception("Deck not found.")
    col.add_note(note, deck_id)

    return note


# NOTE: not used yet
def search_by_platform_id(platform_id: int):
    """Search using tags (faster than field search)"""
    col = get_col()
    return col.find_cards(f"tag:{PLATFORM_TAG_PREFIX}{platform_id}")
