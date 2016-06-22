from addressing import ZeroPageAddressing, AbsoluteAddressing, ImplicitAddressing, ImmediateReadAddressing, \
    ZeroPageAddressingWithX, AbsoluteAddressingWithX, AbsoluteAddressingWithY, IndirectAddressingWithX, \
    IndirectAddressingWithY
from instructions.base_instructions import Bit, StackPush, StackPull, And


# bit instructions
class BitZpg(ZeroPageAddressing, Bit):
    identifier_byte = bytes([0x24])


class BitAbs(AbsoluteAddressing, Bit):
    identifier_byte = bytes([0x2C])


# stack push instructions
class Php(ImplicitAddressing, StackPush):
    identifier_byte = bytes([0x08])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.status_reg.to_int()


class Pha(ImplicitAddressing, StackPush):
    identifier_byte = bytes([0x48])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.a_reg


class Txs(ImplicitAddressing, StackPush):
    identifier_byte = bytes([0x9A])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.x_reg


# stack pull instructions
class Plp(ImplicitAddressing, StackPull):
    identifier_byte = bytes([0x28])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.status_reg.from_int(pulled_data)


class Pla(ImplicitAddressing, StackPull):
    identifier_byte = bytes([0x68])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.a_reg = pulled_data


class Tsx(ImplicitAddressing, StackPull):
    identifier_byte = bytes([0xBA])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.x_reg = pulled_data


# and instructions
class AndImm(ImmediateReadAddressing, And):
    identifier_byte = bytes([0x29])


class AndZpg(ZeroPageAddressing, And):
    identifier_byte = bytes([0x25])


class AndZpgX(ZeroPageAddressingWithX, And):
    identifier_byte = bytes([0x35])


class AndAbs(AbsoluteAddressing, And):
    identifier_byte = bytes([0x2D])


class AndAbsX(AbsoluteAddressingWithX, And):
    identifier_byte = bytes([0x3D])


class AndAbsY(AbsoluteAddressingWithY, And):
    identifier_byte = bytes([0x39])


class AndIndX(IndirectAddressingWithX, And):
    identifier_byte = bytes([0x21])


class AndIndY(IndirectAddressingWithY, And):
    identifier_byte = bytes([0x31])
