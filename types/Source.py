from abc import ABC, abstractmethod

from ..types.AnkiCardModel import AnkiCardModel
from .SourceType import SourceType


class BaseSource(ABC):
    def __init__(self, source_type: SourceType):
        self.source_type = source_type

    @classmethod
    def instance(cls, source_type: SourceType):
        return cls(source_type)

    @abstractmethod
    def scrape(self) -> list[AnkiCardModel]:
        pass
