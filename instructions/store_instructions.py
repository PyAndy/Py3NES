from addressing import ZeroPageAddressing, ZeroPageAddressingWithY, AbsoluteAddressing, ZeroPageAddressingWithX, \
    AbsoluteAddressingWithX, AbsoluteAddressingWithY, IndexedIndirectAddressing, IndirectIndexedAddressing
from instructions.base_instructions import Stx, Sta, Sty


# Stx
class StxZeroPage(ZeroPageAddressing, Stx):
    identifier_byte = bytes([0x86])


class StxZeroPageY(ZeroPageAddressingWithY, Stx):
    identifier_byte = bytes([0x96])


class StxAbs(AbsoluteAddressing, Stx):
    identifier_byte = bytes([0x8E])


# Sta
class StaZpg(ZeroPageAddressing, Sta):
    identifier_byte = bytes([0x85])


class StaZpgX(ZeroPageAddressingWithX, Sta):
    identifier_byte = bytes([0x95])


class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])


class StaAbsX(AbsoluteAddressingWithX, Sta):
    identifier_byte = bytes([0x9D])


class StaAbsY(AbsoluteAddressingWithY, Sta):
    identifier_byte = bytes([0x99])


class StaIndX(IndexedIndirectAddressing, Sta):
    identifier_byte = bytes([0x81])


class StaIndY(IndirectIndexedAddressing, Sta):
    identifier_byte = bytes([0x91])


# Sty
class StyZpg(ZeroPageAddressing, Sty):
    identifier_byte = bytes([0x84])


class StyZpgX(ZeroPageAddressingWithX, Sty):
    identifier_byte = bytes([0x94])


class StyAbs(ZeroPageAddressing, Sty):
    identifier_byte = bytes([0x8C])


