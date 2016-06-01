from typing import List

from memory_owner import MemoryOwnerMixin


class PPU(MemoryOwnerMixin, object):
    memory_start_location = 0x2000
    memory_end_location = 0x2007

    def __init__(self):
        self.memory = [0]*8  # type: List[int]

    def get_memory(self) -> List[int]:
        return self.memory
