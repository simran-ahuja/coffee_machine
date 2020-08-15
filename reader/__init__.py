from abc import ABC, abstractmethod


class IReader(ABC):
    """
    IReader provides interface for innput reader
    """
    @abstractmethod
    def read(self):
        pass
