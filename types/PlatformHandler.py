from abc import ABC, abstractmethod


# 2. The Logic Interface (Strategy)
class PlatformHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        pass
