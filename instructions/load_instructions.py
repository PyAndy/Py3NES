from helpers import generate_classes_from_string
from instructions.base_instructions import Lda, Ldx, Ldy

types = []

lda_types = '''
immidiate     LDA #oper     A9    2     2
zeropage      LDA oper      A5    2     3
zeropage,X    LDA oper,X    B5    2     4
absolute      LDA oper      AD    3     4
absolute,X    LDA oper,X    BD    3     4*
absolute,Y    LDA oper,Y    B9    3     4*
(indirect,X)  LDA (oper,X)  A1    2     6
(indirect),Y  LDA (oper),Y  B1    2     5*
'''

for generated in generate_classes_from_string(Lda, lda_types):
    types.append(generated)


ldx_types = '''
immidiate     LDX #oper     A2    2     2
zeropage      LDX oper      A6    2     3
zeropage,Y    LDX oper,Y    B6    2     4
absolute      LDX oper      AE    3     4
absolute,Y    LDX oper,Y    BE    3     4*
'''

for generated in generate_classes_from_string(Ldx, ldx_types):
    types.append(generated)


ldy_types = '''
immidiate     LDY #oper     A0    2     2
zeropage      LDY oper      A4    2     3
zeropage,X    LDY oper,X    B4    2     4
absolute      LDY oper      AC    3     4
absolute,X    LDY oper,X    BC    3     4*
'''

for generated in generate_classes_from_string(Ldy, ldy_types):
    types.append(generated)
