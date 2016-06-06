from addressing import ImmediateReadAddressing, AbsoluteAddressing, IndexedIndirectAddressing, ZeroPageAddressing, IndirectIndexedAddressing, ZeroPageAddressingWithX, AbsoluteAddressingYOffset, AbsoluteAddressingXOffset
from base_instructions import Lda, Sta, SetBit, ClearBit, Ldx, Ldy
from generic_instructions import register
from status import Status


# Lda
@register
class LdaImm(ImmediateReadAddressing, Lda):
    identifier_byte = bytes([0xA9])


@register
class LdaIndexedIndirect(IndexedIndirectAddressing, Lda):
    identifier_byte = bytes([0xA1])


@register
class LdaZeroPage(ZeroPageAddressing, Lda):
    identifier_byte = bytes([0xA5])


@register
class LdaZeroPageX(ZeroPageAddressingWithX, Lda):
    identifier_byte = bytes([0xB5])


@register
class LdaAbs(AbsoluteAddressing, Lda):
    identifier_byte = bytes([0xAD])


@register
class LdaAbsY(AbsoluteAddressingYOffset, Lda):
    identifier_byte = bytes([0xB9])


@register
class LdaAbsX(AbsoluteAddressingXOffset, Lda):
    identifier_byte = bytes([0xBD])


@register
class LdaIndirectIndexed(IndirectIndexedAddressing, Lda):
    identifier_byte = bytes([0xB1])






@register
class LdxImm(ImmediateReadAddressing, Ldx):
    identifier_byte = bytes([0xA2])


@register
class LdyImm(ImmediateReadAddressing, Ldy):
    identifier_byte = bytes([0xA0])





@register
class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])


# status instructions
@register
class Sei(SetBit):
    identifier_byte = bytes([0x78])
    bit = Status.StatusTypes.interrupt


@register
class Cld(ClearBit):
    identifier_byte = bytes([0xD8])
    bit = Status.StatusTypes.decimal
