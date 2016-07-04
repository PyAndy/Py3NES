from typing import List

from memory_owner import MemoryOwnerMixin


class APU(MemoryOwnerMixin, object):
    memory_start_location = 0x4000
    memory_end_location = 0x401F

    def __init__(self):
        self.memory = [0]*0x20  # type: List[int]

    def get_memory(self) -> List[int]:
        return self.memory
