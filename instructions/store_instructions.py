from addressing import ZeroPageAddressing, ZeroPageAddressingWithY, AbsoluteAddressing, ZeroPageAddressingWithX, \
    AbsoluteAddressingWithX, AbsoluteAddressingWithY, IndirectAddressingWithX, IndirectAddressingWithY
from helpers import generate_classes_from_string
from instructions.base_instructions import Stx, Sta, Sty

types = []

# stx
stx_types = '''
zeropage      STX oper      86    2     3
zeropage,Y    STX oper,Y    96    2     4
absolute      STX oper      8E    3     4
'''

for generated in generate_classes_from_string(Stx, stx_types):
    types.append(generated)


# Sta
sta_types = '''
zeropage      STA oper      85    2     3
zeropage,X    STA oper,X    95    2     4
absolute      STA oper      8D    3     4
absolute,X    STA oper,X    9D    3     5
absolute,Y    STA oper,Y    99    3     5
(indirect,X)  STA (oper,X)  81    2     6
(indirect),Y  STA (oper),Y  91    2     6
'''

for generated in generate_classes_from_string(Sta, sta_types):
    types.append(generated)


# Sty
sty_types = '''
zeropage      STY oper      84    2     3
zeropage,X    STY oper,X    94    2     4
absolute      STY oper      8C    3     4
'''

for generated in generate_classes_from_string(Sty, sty_types):
    types.append(generated)