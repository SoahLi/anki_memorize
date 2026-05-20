# 4. The Registry (The "Brain")
from typing import Dict

from platform_handlers.youtube.Youtube import Youtube
from custom_types.PlatformHandler import PlatformHandler

PLATFORM_LOGIC_MAP: Dict[str, PlatformHandler] = {}


def init_platform_registry(youtube_platform_id: int):
    # initialize all platform handlers with their respective platform ids
    PLATFORM_LOGIC_MAP["youtube"] = Youtube(youtube_platform_id)
