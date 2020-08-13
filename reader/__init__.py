from abc import ABC, abstractmethod


class IReader(ABC):
    @abstractmethod
    def read(self):
        pass
