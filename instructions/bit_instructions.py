import numpy as np

from addressing import ImplicitAddressing
from instructions.base_instructions import StackPush, StackPull, RegisterModifier


# stack push instructions
from instructions.generic_instructions import Instruction


class Php(ImplicitAddressing, StackPush):
    """
    N Z C I D V
    - - - - - -
    """
    identifier_byte = bytes([0x08])

    @classmethod
    def data_to_push(cls, cpu):
        # set bit 4 and 5 to be 1, see: http://wiki.nesdev.com/w/index.php/CPU_status_flag_behavior
        return cpu.status_reg.to_int() | 0b110000


class Pha(ImplicitAddressing, StackPush):
    """
    N Z C I D V
    - - - - - -
    """
    identifier_byte = bytes([0x48])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.a_reg


class Txs(ImplicitAddressing, Instruction):
    """
    N Z C I D V
    + + - - - -
    """
    # TODO: does not set negative
    # sets_negative_bit = True
    sets_zero_bit = True

    identifier_byte = bytes([0x9A])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.sp_reg = cpu.x_reg
        return cpu.sp_reg


# stack pull instructions
class Plp(ImplicitAddressing, StackPull):
    """
    sets the stack
    ignores bits 4 and 5
    """
    identifier_byte = bytes([0x28])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.status_reg.from_int(pulled_data, [4, 5])


class Pla(ImplicitAddressing, StackPull):
    """
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    identifier_byte = bytes([0x68])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.a_reg = np.uint8(pulled_data)
        return cpu.a_reg


class Tsx(ImplicitAddressing, Instruction):
    """
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    identifier_byte = bytes([0xBA])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = cpu.sp_reg
        return cpu.x_reg


# register instructions
class Iny(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xC8])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg += np.uint8(1)
        return cpu.y_reg


class Dey(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0x88])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg -= np.uint8(1)
        return cpu.y_reg


class Inx(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xE8])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg += np.uint8(1)
        return cpu.x_reg


class Dex(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xCA])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg -= np.uint8(1)
        return cpu.x_reg


class Tax(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xAA])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = cpu.a_reg
        return cpu.x_reg


class Txa(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0x8A])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = cpu.x_reg
        return cpu.a_reg


class Tay(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xA8])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = cpu.a_reg
        return cpu.y_reg


class Tya(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0x98])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = cpu.y_reg
        return cpu.a_reg
