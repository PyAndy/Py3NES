from typing import Optional

import numpy as np

import cpu as c


class Addressing(object):
    data_length = 0

    @classmethod
    def get_instruction_length(cls):
        return cls.data_length + 1

    @classmethod
    def get_offset(cls, cpu):
        return 0


class XRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return cpu.x_reg


class YRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return cpu.y_reg


class ImplicitAddressing(Addressing):
    """
    instructions that have data passed
    example: CLD
    """
    data_length = 0


class AccumulatorAddressing(Addressing):
    """
    get value from accumulator
    """
    data_length = 0

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg


class ImmediateReadAddressing(Addressing):
    """
    read a value from the instruction data
    example: STA #7
    example: 8D 07
    """
    data_length = 1

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return data_bytes[0]


class AbsoluteAddressing(Addressing):
    """
    looks up an absolute memory address and returns the value
    example: STA $12 34
    example: 8D 34 12
    """
    data_length = 2

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        return np.uint16(int.from_bytes(data_bytes, byteorder='little') + cls.get_offset(cpu))


class AbsoluteAddressingWithX(XRegOffset, AbsoluteAddressing):
    """
    adds the x reg offset to an absolute memory location
    """


class AbsoluteAddressingWithY(YRegOffset, AbsoluteAddressing):
    """
    adds the y reg offset to an absolute memory location
    """


class ZeroPageAddressing(Addressing):
    """
    look up an absolute memory address in the first 256 bytes
    example: STA $12
    memory_address: $12
    Note: can overflow
    """
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        address = np.uint8(int.from_bytes(data_bytes, byteorder='little') + cls.get_offset(cpu))

        return address


class ZeroPageAddressingWithX(XRegOffset, ZeroPageAddressing):
    """
    adds the x reg offset to an absolute memory address in the first 256 bytes
    """


class ZeroPageAddressingWithY(YRegOffset, ZeroPageAddressing):
    """
    adds the y reg offset to an absolute memory address in the first 256 bytes
    """


class RelativeAddressing(Addressing):
    """
    offset from current PC, can only jump 128 bytes in either direction
    """
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        # get the program counter
        current_address = cpu.pc_reg

        # offset by value in instruction
        return current_address + np.uint16(int.from_bytes(data_bytes, byteorder='little'))


class IndirectBase(Addressing):
    @classmethod
    def get_address(cls, cpu: 'c.CPU', data_bytes: bytes):
        # look up the bytes at [original_address, original_address + 1]
        lsb_location = np.uint16(super().get_address(cpu, data_bytes))
        msb_location = np.uint16(lsb_location + 1)

        # wrap around on page boundaries
        if msb_location % 0x100 == 0:
            msb_location = np.uint16(lsb_location - 0xFF)

        lsb = cpu.get_memory(lsb_location)
        msb = cpu.get_memory(msb_location)

        return np.uint16(int.from_bytes(bytes([lsb, msb]), byteorder='little'))


class IndirectAddressing(IndirectBase, AbsoluteAddressing):
    """
    indirect address
    """


class IndirectAddressingWithX(IndirectBase, ZeroPageAddressingWithX):
    """
    adds the x reg before indirection
    """


class IndirectAddressingWithY(IndirectBase, ZeroPageAddressing):
    """
    adds the y reg after indirection
    """

    @classmethod
    def get_address(cls, cpu: 'c.CPU', data_bytes: bytes):
        return np.uint16(super().get_address(cpu, data_bytes) + cpu.y_reg)
