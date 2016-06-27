import numpy as np

import cpu as c
from addressing import ImplicitAddressing, RelativeAddressing
from helpers import Numbers
from instructions.generic_instructions import Instruction, WritesToMem, ReadsFromMem
from status import Status


class Jmp(Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.pc_reg = memory_address


class Jsr(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # store the pc reg on the stack
        cpu.set_memory(cpu.sp_reg, cpu.pc_reg, num_bytes=Numbers.SHORT.value)

        # increases the size of the stack
        cpu.increase_stack_size(Numbers.SHORT.value)

        # jump to the memory location
        super().write(cpu, memory_address, value)


class Rts(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # decrease the size of the stack
        cpu.decrease_stack_size(Numbers.SHORT.value)

        # grab the stored pc reg from the stack
        old_pc_reg = cpu.get_memory(cpu.sp_reg, num_bytes=Numbers.SHORT.value)

        # jump to the memory location
        super().write(cpu, old_pc_reg, value)


class BranchClear(RelativeAddressing, Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        if not cpu.status_reg.bits[cls.bit]:
            super().write(cpu, memory_address, value)


class BranchSet(RelativeAddressing, Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        if cpu.status_reg.bits[cls.bit]:
            super().write(cpu, memory_address, value)


class Nop(Instruction):
    """
    N Z C I D V
    - - - - - -
    """


class Bit(ReadsFromMem, Instruction):
    """
    N Z C I D V
    + x - - - +
    """
    sets_negative_bit = True
    sets_overflow_bit_from_value = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # set the zero flag based on value & a_reg
        cpu.status_reg.bits[Status.StatusTypes.zero] = not bool(value & cpu.a_reg)


class Ld(ReadsFromMem, Instruction):
    """
    N Z C I D V
    + + - - - -
    """
    sets_zero_bit = True
    sets_negative_bit = True


class Lda(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        if memory_address == 0x0180:
            cpu.get_memory(memory_address)
        cpu.a_reg = np.uint8(value)


class Ldx(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = np.uint8(value)


class Ldy(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = np.uint8(value)


class Sta(WritesToMem, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg


class Stx(WritesToMem, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.x_reg


class Sty(WritesToMem, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.y_reg


class And(Instruction):
    """
    bitwise and with accumulator and store result
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg &= value
        return cpu.a_reg


class Or(Instruction):
    """
    bitwise or with accumulator and store result
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg |= value
        return cpu.a_reg


class Eor(Instruction):
    """
    bitwise exclusive or with accumulator and store result
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg ^= value
        return cpu.a_reg


class Adc(Instruction):
    """
    A + M + C -> A, C
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        result = cpu.a_reg + value + int(cpu.status_reg.bits[Status.StatusTypes.carry])
        # if value and a_reg have different signs than result, set overflow
        overflow = bool((cpu.a_reg ^ result) & (value ^ result) & 0x80)
        cpu.status_reg.bits[Status.StatusTypes.overflow] = overflow

        # if greater than 255, carry
        if result >= 256:
            result %= 256
            cpu.status_reg.bits[Status.StatusTypes.carry] = True
        else:
            cpu.status_reg.bits[Status.StatusTypes.carry] = False

        cpu.a_reg = result
        return cpu.a_reg


class Sbc(Adc):
    """
    A - M - C -> A
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        return super().write(cpu, memory_address, value ^ 0xFF)


class Compare(Instruction):
    """
    compare given value with a given reg
    N Z C I D V
    + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.status_reg.bits[Status.StatusTypes.carry] = not bool(value & 256)
        return value


class Cmp(Compare):
    """
    compare given value with the a reg
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        result = cpu.a_reg - value
        return super().write(cpu, memory_address, result)


class Cpx(Compare):
    """
    compare given value with the x reg
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        result = cpu.x_reg - value
        return super().write(cpu, memory_address, result)


class Cpy(Compare):
    """
    compare given value with the y reg
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        result = cpu.y_reg - value
        return super().write(cpu, memory_address, result)


class StackPush(Instruction):
    """
    pushes data onto stack
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # grab the data to write
        data_to_push = cls.data_to_push(cpu)

        # write the data to the stack
        cpu.set_memory(cpu.sp_reg, data_to_push)

        # increases the size of the stack
        cpu.increase_stack_size(Numbers.BYTE.value)

        return data_to_push


class StackPull(Instruction):
    """
    pulls data from the stack
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # decrease the size of the stack
        cpu.decrease_stack_size(Numbers.BYTE.value)

        # get the data from the stack
        pulled_data = cpu.get_memory(cpu.sp_reg)

        # write the pulled data
        return cls.write_pulled_data(cpu, pulled_data)


class RegisterModifier(Instruction):
    """
    updates register
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True


class SetBit(ImplicitAddressing, Instruction):
    """
    sets a bit to be True in the status reg
    N Z C I D V
    x x x x x x
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.bits[cls.bit] = True


class ClearBit(ImplicitAddressing, Instruction):
    """
    sets a bit to be False in the status reg
    N Z C I D V
    x x x x x x
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'c.CPU'):
        cpu.status_reg.bits[cls.bit] = False
