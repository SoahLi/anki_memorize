from typing import Any, Dict, Optional

import aqt

Config = Dict[str, Any]


def config() -> Optional[Config]:
    if not aqt.mw:
        return None
    return aqt.mw.addonManager.getConfig(__name__)


def config_get(key: str):
    config_snapshot = config()
    print(f"Config snapshot: {config_snapshot}")
    if not config_snapshot:
        return None
    return config_snapshot.get(key)


def config_get_ensure_exists(key: str) -> str:
    config_snapshot = config()
    if not config_snapshot:
        raise Exception("Config not available.")
    result = config_snapshot.get(key)
    if result is None:
        raise Exception(f"Config key '{key}' not found.")
    return result
