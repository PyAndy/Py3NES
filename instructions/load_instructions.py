from addressing import ImmediateReadAddressing, IndexedIndirectAddressing, ZeroPageAddressing, ZeroPageAddressingWithX, \
    AbsoluteAddressing, AbsoluteAddressingWithY, AbsoluteAddressingWithX, IndirectIndexedAddressing, \
    ZeroPageAddressingWithY
from instructions.base_instructions import Lda, Ldx, Ldy


# Lda
class LdaImm(ImmediateReadAddressing, Lda):
    identifier_byte = bytes([0xA9])


class LdaIndexedIndirect(IndexedIndirectAddressing, Lda):
    identifier_byte = bytes([0xA1])


class LdaZeroPage(ZeroPageAddressing, Lda):
    identifier_byte = bytes([0xA5])


class LdaZeroPageX(ZeroPageAddressingWithX, Lda):
    identifier_byte = bytes([0xB5])


class LdaAbs(AbsoluteAddressing, Lda):
    identifier_byte = bytes([0xAD])


class LdaAbsY(AbsoluteAddressingWithY, Lda):
    identifier_byte = bytes([0xB9])


class LdaAbsX(AbsoluteAddressingWithX, Lda):
    identifier_byte = bytes([0xBD])


class LdaIndirectIndexed(IndirectIndexedAddressing, Lda):
    identifier_byte = bytes([0xB1])


# Ldx
class LdxImm(ImmediateReadAddressing, Ldx):
    identifier_byte = bytes([0xA2])


class LdxZpg(ZeroPageAddressing, Ldx):
    identifier_byte = bytes([0xA6])


class LdxZpgY(ZeroPageAddressingWithY, Ldx):
    identifier_byte = bytes([0xB6])


class LdxAbs(AbsoluteAddressing, Ldx):
    identifier_byte = bytes([0xAE])


class LdxAbsY(AbsoluteAddressingWithY, Ldx):
    identifier_byte = bytes([0xBE])


# Ldy
class LdyImm(ImmediateReadAddressing, Ldy):
    identifier_byte = bytes([0xA0])


class LdyZpg(ZeroPageAddressing, Ldy):
    identifier_byte = bytes([0xA4])


class LdyZpgX(ZeroPageAddressingWithX, Ldy):
    identifier_byte = bytes([0xB4])


class LdyAbs(AbsoluteAddressing, Ldy):
    identifier_byte = bytes([0xAC])


class LdyAbsX(AbsoluteAddressingWithX, Ldy):
    identifier_byte = bytes([0xBC])
