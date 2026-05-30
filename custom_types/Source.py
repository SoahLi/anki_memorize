from abc import ABC, abstractmethod

from custom_types.Item import Item
from custom_types.SourceType import SourceType
from util.config import config_get


class BaseSource(ABC):
    def __init__(self, source_type: SourceType, platform_id: int):
        self.source_type = source_type
        self.platform_id = platform_id
        self.page_size: int = int(config_get("page_size", "10"))

    @classmethod
    def instance(cls, source_type: SourceType, platform_id: int):
        return cls(source_type, platform_id)

    @abstractmethod
    def scrape(self) -> list[Item]:
        pass
