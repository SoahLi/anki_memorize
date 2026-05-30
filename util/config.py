from typing import Any, Dict, Optional

import aqt

from custom_types.SourceType import SourceType

Config = Dict[str, Any]


import os
import json

def config() -> Optional[Config]:
    # Try to use Anki's config API if available
    if hasattr(aqt, 'mw') and aqt.mw:
        return aqt.mw.addonManager.getConfig("anki_memorize")
    # Fallback: load config.json directly from the add-on directory
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
    # Use the add-on folder name to get the config
    return aqt.mw.addonManager.getConfig("anki_memorize")


def config_get(key: str, default: Optional[Any] = None) -> Any:
    config_snapshot = config()
    print(f"Config snapshot: {config_snapshot}")
    if not config_snapshot:
        print("Config not available, returning default.")
        return default
    result = config_snapshot.get(key)
    if result is None:
        print(f"Config key '{key}' not found, returning default.")
    return result if result is not None else default


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
