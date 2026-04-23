from abc import ABC, abstractmethod


# 2. The Logic Interface (Strategy)
class PlatformHandler(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def update(self):
        pass
