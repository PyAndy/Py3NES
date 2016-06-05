from abc import ABC, abstractproperty
from typing import Optional, List

import cpu as c
from addressing import ImmediateReadAddressingMixin, NoAddressingMixin, AbsoluteAddressingMixin


def writes_to_memory(cls):
    cls._writes_to_memory = True
    return cls


class Instruction(ABC):
    _writes_to_memory = False

    def __init__(self):
        pass

    def __str__(self):
        return "{}, Identifier byte: {}".format(self.__class__.__name__,
                                                self.identifier_byte)

    @abstractproperty
    @property
    def identifier_byte(self) -> bytes:
        return None

    def get_address(self, data_bytes: bytes) -> Optional[int]:
        return None

    def apply_side_effects(self, cpu: 'c.CPU'):
        pass

    def get_data(self, cpu, memory_address, data_bytes) -> Optional[int]:
        return None

    def write(self, cpu, memory_address, value):
        if self._writes_to_memory:
            memory_owner = cpu.get_memory_owner(memory_address)
            memory_owner.set(memory_address, value)

    def execute(self, cpu: 'c.CPU', data_bytes: bytes):
        memory_address = self.get_address(data_bytes)

        value = self.get_data(cpu, memory_address, data_bytes)

        self.write(cpu, memory_address, value)

        self.apply_side_effects(cpu)


# write function
class LdaImmInstruction(ImmediateReadAddressingMixin, Instruction):
    identifier_byte = bytes([0xA9])

    def write(self, cpu, memory_address, value):
        cpu.a_reg = value


@writes_to_memory
class StaAbsInstruction(AbsoluteAddressingMixin, Instruction):
    identifier_byte = bytes([0x8D])

    def get_data(self, cpu, memory_address, data_bytes):
        return cpu.a_reg


# status instructions
class SeiInstruction(NoAddressingMixin, Instruction):
    identifier_byte = bytes([0x78])

    def apply_side_effects(self, cpu: 'c.CPU'):
        # set the instruction flag to 1
        cpu.status_reg.interrupt_bit = True


class CldInstruction(NoAddressingMixin, Instruction):
    identifier_byte = bytes([0xD8])

    def apply_side_effects(self, cpu: 'c.CPU'):
        cpu.status_reg.decimal_bit = False
