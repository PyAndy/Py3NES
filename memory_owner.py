from abc import abstractmethod, ABC, abstractproperty
from typing import List


class MemoryOwnerMixin(ABC):
    # TODO check we have correct amount of memory
    @abstractproperty
    @property
    def memory_start_location(self) -> int:
        """
        inclusive
        """
        pass

    @abstractproperty
    @property
    def memory_end_location(self) -> int:
        """
        inclusive
        """
        pass

    @abstractmethod
    def get_memory(self) -> List[int]:
        pass

    def get(self, position: int) -> int:
        """
        gets int at given position
        """
        return self.get_memory()[position - self.memory_start_location]

    def set(self, position: int, value: int):
        """
        sets int at given position
        """
        self.get_memory()[position - self.memory_start_location] = value
