from typing import Optional


from custom_types.PlatformHandler import PlatformHandler
from util.platform_registry import PLATFORM_LOGIC_MAP


def get_platform_handler_by_name(name: str) -> Optional[PlatformHandler]:
    return PLATFORM_LOGIC_MAP.get(name)
