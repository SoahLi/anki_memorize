from ..util.config import config_get
from ..util.getters import get_platform_by_name


def update_deck():
    platforms: list[str] = config_get("platforms") or []

    for platform_name in platforms:
        platform = get_platform_by_name(platform_name)
        platform.handler.update()
