from typing import List

from memory_owner import MemoryOwnerMixin

KB_SIZE = 1024


class ROM(MemoryOwnerMixin, object):
    # rom memory is duplicated around 0xC000
    memory_start_location = 0x8000
    memory_end_location = 0xFFFF

    def __init__(self, rom_bytes: bytes):
        self.header_size = 0x10

        # TODO unhardcode, pull from rom header
        self.num_prg_blocks = 2

        # program data starts after header
        # and lasts for a set number of 16KB blocks
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:
                                   self.header_size + (16 * KB_SIZE * self.num_prg_blocks)]

    def get_memory(self) -> List[bytes]:
        return self.prg_bytes

    def get(self, position: int, size: int=1) -> bytes:
        """
        gets bytes at given position, could be multiple bytes
        memory is duplicated around 0xC000
        """
        if position >= 0xC000:
            position -= 0x4000
        return self.get_memory()[position-self.memory_start_location:position-self.memory_start_location+size]

    def set(self, position: int, value: int):
        raise Exception('Cant set read only memory')
