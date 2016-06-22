from addressing import AbsoluteAddressing, IndirectAddressing, ImplicitAddressing
from instructions.base_instructions import Jmp, Jsr, BranchSet, BranchClear, Rts

# Jmp
from status import Status


class JmpAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x4C])


class JmpInd(IndirectAddressing, Jmp):
    identifier_byte = bytes([0x6C])


# Jsr and Rts
class JsrAbs(AbsoluteAddressing, Jsr):
    identifier_byte = bytes([0x20])


class RtsImp(ImplicitAddressing, Rts):
    identifier_byte = bytes([0x60])


# branch sets
class Bcs(BranchSet):
    identifier_byte = bytes([0xB0])
    bit = Status.StatusTypes.carry


class BEQ(BranchSet):
    identifier_byte = bytes([0xF0])
    bit = Status.StatusTypes.zero


class BMI(BranchSet):
    identifier_byte = bytes([0x30])
    bit = Status.StatusTypes.negative


class BVS(BranchSet):
    identifier_byte = bytes([0x70])
    bit = Status.StatusTypes.overflow


# branch clears
class BVC(BranchClear):
    identifier_byte = bytes([0x50])
    bit = Status.StatusTypes.overflow


class BNE(BranchClear):
    identifier_byte = bytes([0xD0])
    bit = Status.StatusTypes.zero


class Bcc(BranchClear):
    identifier_byte = bytes([0x90])
    bit = Status.StatusTypes.carry


class BPL(BranchClear):
    identifier_byte = bytes([0x10])
    bit = Status.StatusTypes.negative
