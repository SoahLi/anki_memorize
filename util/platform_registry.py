# 4. The Registry (The "Brain")
from typing import Dict

from ..handlers.Youtube import Youtube
from ..types.PlatformHandler import PlatformHandler

PLATFORM_LOGIC_MAP: Dict[str, PlatformHandler] = {
    "youtube": Youtube(),
}
