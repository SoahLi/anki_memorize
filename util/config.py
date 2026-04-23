from typing import Any, Dict, Optional

import aqt

from ..types.SourceType import SourceType

Config = Dict[str, Any]


def config() -> Optional[Config]:
    if not aqt.mw:
        return None
    return aqt.mw.addonManager.getConfig(__name__)


def config_get(key: str) -> Any:
    config_snapshot = config()
    print(f"Config snapshot: {config_snapshot}")
    if not config_snapshot:
        return None
    return config_snapshot.get(key)


def config_get_ensure_exists(key: str) -> Any:
    config_snapshot = config()
    if not config_snapshot:
        raise Exception("Config not available.")
    result = config_snapshot.get(key)
    if result is None:
        raise Exception(f"Config key '{key}' not found.")
    return result


def config_get_source_types_for_platform(platform: str) -> Optional[list[SourceType]]:
    platforms = config_get("platforms")
    platform_config = platforms.get(platform) if platforms else None
    if not platform_config:
        return None

    sources = platform_config.get("sources")
    if not sources:
        return None

    sources = [SourceType(s) for s in sources]

    return sources
