from abc import ABC, abstractmethod

from ..types.Item import Item
from .SourceType import SourceType


class BaseSource(ABC):
    def __init__(self, source_type: SourceType, platform_id: int):
        self.source_type = source_type
        self.platform_id = platform_id

    @classmethod
    def instance(cls, source_type: SourceType, platform_id: int):
        return cls(source_type, platform_id)

    @abstractmethod
    def scrape(self) -> list[Item]:
        pass
