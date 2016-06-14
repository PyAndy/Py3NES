from addressing import ImplicitAddressing
from generic_instructions import Instruction, WritesToMem
import cpu as c


class Jmp(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.pc_reg = memory_address


class Jsr(Jmp):
    @classmethod
    def write(cls, cpu, memory_address, value):
        # store the pc reg on the stack
        memory_owner = cpu.get_memory_owner(cpu.sp_reg)
        memory_owner.set(cpu.sp_reg, cpu.pc_reg, 2)

        # increases the size of the stack
        cpu.sp_reg -= 2

        # jump to the memory location
        super().write(cpu, memory_address, value)


class Lda(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ldx(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Ldy(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value


class Sta(WritesToMem, Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg


class Stx(WritesToMem, Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.x_reg


class Sty(WritesToMem, Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.y_reg


class SetBit(ImplicitAddressing, Instruction):
    """
    sets a bit to be True
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.interrupt_bit = True


class ClearBit(ImplicitAddressing, Instruction):
    """
    sets a bit to be False
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.interrupt_bit = False
