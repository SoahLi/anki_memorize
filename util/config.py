from typing import Dict, Optional

import aqt

Config = Dict[str, str]


def config() -> Optional[Config]:
    if not aqt.mw:
        return None
    return aqt.mw.addonManager.getConfig(__name__)


def get_config(key: str) -> Optional[str]:
    config_snapshot = config()
    if not config_snapshot:
        return None
    return config_snapshot.get(key)
