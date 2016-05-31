KB_SIZE = 1024


class ROM(object):
    def __init__(self, rom_bytes: bytes):
        self.header_size = 16

        # TODO unhardcode, pull from rom header
        self.num_prg_blocks = 2

        # program data starts after header
        # and lasts for a set number of 16KB blocks
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:
                                   self.header_size + (16 * KB_SIZE * self.num_prg_blocks)]

    def get_byte(self, position: int) -> bytes:
        """
        gets byte at given position
        """
        return self.rom_bytes[position:position+1]
