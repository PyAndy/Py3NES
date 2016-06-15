from typing import Optional
import cpu as c


class Instruction:
    identifier_byte = None
    sets_zero_bit = False
    sets_negative_bit = False

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        return None

    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        pass

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return None

    @classmethod
    def write(cls, cpu, memory_address, value):
        pass

    @classmethod
    def execute(cls, cpu: 'c.CPU', data_bytes: bytes):
        memory_address = cls.get_address(cpu, data_bytes)

        value = cls.get_data(cpu, memory_address, data_bytes)

        cls.write(cpu, memory_address, value)

        cls.apply_side_effects(cpu)

        return value


class WritesToMem(object):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.set_memory(memory_address, value)
