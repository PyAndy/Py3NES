from typing import List, Optional


class AddressingMixin(object):
    data_length = 0

    @property
    def instruction_length(self):
        return self.data_length + 1


class NoAddressingMixin(AddressingMixin):
    """
    instructions that have data passed
    example: CLD
    """
    data_length = 0


class ImmediateReadAddressingMixin(AddressingMixin):
    """
    read a value from the instruction data
    example: STA #7
    example: 8D 07
    """
    data_length = 1

    def get_data(self, cpu, memory_address, data_bytes):
        return data_bytes[0]


class AbsoluteAddressingMixin(AddressingMixin):
    """
    looks up an absolute memory address and returns the value
    example: STA $12 34
    example: 8D 34 12
    """
    data_length = 2

    def get_address(self, data_bytes: bytes) -> Optional[int]:
        return int.from_bytes(data_bytes, byteorder='little')


# TODO this is not real yet
# class AbsoluteAddressingWithXMixin(AddressingMixin):
#     """
#     looks up an absolute memory address including adding the x reg to that address
#     returns the value at that address
#     example: STA $12 34
#     memory_address = ($3412+#X)
#     """
#     data_length = 2
#
#     def get_address(self, data_bytes: bytes) -> Optional[int]:
#         return int.from_bytes(data_bytes, byteorder='little')
