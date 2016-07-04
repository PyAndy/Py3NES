from helpers import generate_classes_from_string
from instructions.base_instructions import SetBit, ClearBit, Nop
from status import Status


types = []


# Nop
nop_types = '''
implied       NOP           EA    1     2
implied       NOP           1A    1     2
implied       NOP           3A    1     2
implied       NOP           5A    1     2
implied       NOP           7A    1     2
implied       NOP           DA    1     2
implied       NOP           FA    1     2
immidiate     NOP #oper     80    2     2
immidiate     NOP #oper     82    2     2
immidiate     NOP #oper     89    2     2
immidiate     NOP #oper     C2    2     2
immidiate     NOP #oper     E2    2     2
zeropage      NOP oper      04    2     3
zeropage      NOP oper      44    2     3
zeropage      NOP oper      64    2     3
absolute      NOP oper      0C    3     4
zeropage,X    NOP oper,X    14    2     4
zeropage,X    NOP oper,X    34    2     4
zeropage,X    NOP oper,X    54    2     4
zeropage,X    NOP oper,X    74    2     4
zeropage,X    NOP oper,X    D4    2     4
zeropage,X    NOP oper,X    F4    2     4
absolute,X    NOP oper,X    1C    3     4*
absolute,X    NOP oper,X    3C    3     4*
absolute,X    NOP oper,X    5C    3     4*
absolute,X    NOP oper,X    7C    3     4*
absolute,X    NOP oper,X    DC    3     4*
absolute,X    NOP oper,X    FC    3     4*
'''

for generated in generate_classes_from_string(Nop, nop_types):
    types.append(generated)


# set status instructions
class Sec(SetBit):
    identifier_byte = bytes([0x38])
    bit = Status.StatusTypes.carry


class Sei(SetBit):
    identifier_byte = bytes([0x78])
    bit = Status.StatusTypes.interrupt


class Sed(SetBit):
    identifier_byte = bytes([0xF8])
    bit = Status.StatusTypes.decimal


# clear status instructions
class Cld(ClearBit):
    identifier_byte = bytes([0xD8])
    bit = Status.StatusTypes.decimal


class Clv(ClearBit):
    identifier_byte = bytes([0xB8])
    bit = Status.StatusTypes.overflow


class Clc(ClearBit):
    identifier_byte = bytes([0x18])
    bit = Status.StatusTypes.carry


class Cli(ClearBit):
    identifier_byte = bytes([0x58])
    bit = Status.StatusTypes.interrupt
