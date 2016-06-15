from abc import abstractmethod, ABC, abstractproperty
from typing import List

from helpers import short_to_bytes, Numbers


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

    def get(self, position: int):
        """
        gets int at given position
        """
        return self.get_memory()[position - self.memory_start_location]

    def set(self, position: int, value: int, size: int=1):
        """
        sets int at given position
        """
        if size == Numbers.BYTE:
            self.get_memory()[position - self.memory_start_location] = value
        elif size == Numbers.SHORT:
            upper, lower = short_to_bytes(value)
            self.get_memory()[position - self.memory_start_location] = upper
            self.get_memory()[position - self.memory_start_location - 1] = lower
