from addressing import ImmediateReadAddressing, AbsoluteAddressing, IndexedIndirectAddressing, ZeroPageAddressing, IndirectIndexedAddressing, ZeroPageAddressingWithX, AbsoluteAddressingYOffset, AbsoluteAddressingXOffset, \
    ZeroPageAddressingWithY
from base_instructions import Lda, Sta, SetBit, ClearBit, Ldx, Ldy, Jmp, Stx, Jsr
from status import Status


# Jmp
class JmpAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x4C])


# Jsr
class JsrAbs(AbsoluteAddressing, Jsr):
    identifier_byte = bytes([0x20])


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


class LdaAbsY(AbsoluteAddressingYOffset, Lda):
    identifier_byte = bytes([0xB9])


class LdaAbsX(AbsoluteAddressingXOffset, Lda):
    identifier_byte = bytes([0xBD])


class LdaIndirectIndexed(IndirectIndexedAddressing, Lda):
    identifier_byte = bytes([0xB1])




# Ldx
class LdxImm(ImmediateReadAddressing, Ldx):
    identifier_byte = bytes([0xA2])


#Ldy
class LdyImm(ImmediateReadAddressing, Ldy):
    identifier_byte = bytes([0xA0])


# Stx
class StxZeroPage(ZeroPageAddressing, Stx):
    identifier_byte = bytes([0x86])


class StxZeroPageY(ZeroPageAddressingWithY, Stx):
    identifier_byte = bytes([0x96])


class StxAbs(AbsoluteAddressing, Stx):
    identifier_byte = bytes([0x8E])



# Sta
class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])


# status instructions
class Sei(SetBit):
    identifier_byte = bytes([0x78])
    bit = Status.StatusTypes.interrupt


class Cld(ClearBit):
    identifier_byte = bytes([0xD8])
    bit = Status.StatusTypes.decimal
