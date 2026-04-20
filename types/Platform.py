from sqlmodel import Field, SQLModel

from ..util.platform_registry import PLATFORM_LOGIC_MAP
from .PlatformHandler import PlatformHandler


# 1. The Pure Data Model
class Platform(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str  # e.g., "youtube"

    @property
    def handler(self):
        return get_handler(self)


def get_handler(platform: Platform) -> PlatformHandler:
    handler = PLATFORM_LOGIC_MAP.get(platform.name.lower())
    if not handler:
        raise ValueError(f"No logic implemented for {platform.name}")
    return handler
