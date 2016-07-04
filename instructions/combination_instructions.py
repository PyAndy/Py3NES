from helpers import generate_classes_from_string
from instructions.base_instructions import Lax, Sax, Dcp, Isb, Slo, Rla, Rra, Sre

types = []

lax_types = '''
zeropage      LAX oper      A7    2     3
absolute      LAX oper      AF    3     4
(indirect,X)  LAX (oper,X)  A3    2     6
(indirect),Y  LAX (oper),Y  B3    2     5*
zeropage,Y    LAX oper,Y    B7    2     4
absolute,Y    LAX oper,Y    BF    3     4*
'''

for generated in generate_classes_from_string(Lax, lax_types):
    types.append(generated)

sax_types = '''
(indirect,X)  SAX (oper,X)  83    2     6
zeropage      SAX oper      87    2     3
absolute      SAX oper      8F    3     4
zeropage,Y    SAX oper,Y    97    2     4
'''

for generated in generate_classes_from_string(Sax, sax_types):
    types.append(generated)

dcp_types = '''
(indirect,X)  DCP (oper,X)  C3    2     6
zeropage      DCP oper      C7    2     3
absolute      DCP oper      CF    3     4
(indirect),Y  DCP (oper),Y  D3    2     5*
zeropage,X    DCP oper,X    D7    2     4
absolute,Y    DCP oper,Y    DB    3     4*
absolute,X    DCP oper,X    DF    3     4*
'''

for generated in generate_classes_from_string(Dcp, dcp_types):
    types.append(generated)

isb_types = '''
(indirect,X)  ISB (oper,X)  E3    2     6
zeropage      ISB oper      E7    2     3
absolute      ISB oper      EF    3     4
(indirect),Y  ISB (oper),Y  F3    2     5*
zeropage,X    ISB oper,X    F7    2     4
absolute,Y    ISB oper,Y    FB    3     4*
absolute,X    ISB oper,X    FF    3     4*
'''

for generated in generate_classes_from_string(Isb, isb_types):
    types.append(generated)

slo_types = '''
(indirect,X)  SLO (oper,X)  03    2     6
zeropage      SLO oper      07    2     3
absolute      SLO oper      0F    3     4
(indirect),Y  SLO (oper),Y  13    2     5*
zeropage,X    SLO oper,X    17    2     4
absolute,Y    SLO oper,Y    1B    3     4*
absolute,X    SLO oper,X    1F    3     4*
'''

for generated in generate_classes_from_string(Slo, slo_types):
    types.append(generated)

rla_types = '''
(indirect,X)  RLA (oper,X)  23    2     6
zeropage      RLA oper      27    2     3
absolute      RLA oper      2F    3     4
(indirect),Y  RLA (oper),Y  33    2     5*
zeropage,X    RLA oper,X    37    2     4
absolute,Y    RLA oper,Y    3B    3     4*
absolute,X    RLA oper,X    3F    3     4*
'''

for generated in generate_classes_from_string(Rla, rla_types):
    types.append(generated)

rra_types = '''
(indirect,X)  RRA (oper,X)  63    2     6
zeropage      RRA oper      67    2     3
absolute      RRA oper      6F    3     4
(indirect),Y  RRA (oper),Y  73    2     5*
zeropage,X    RRA oper,X    77    2     4
absolute,Y    RRA oper,Y    7B    3     4*
absolute,X    RRA oper,X    7F    3     4*
'''

for generated in generate_classes_from_string(Rra, rra_types):
    types.append(generated)

sre_types = '''
(indirect,X)  SRE (oper,X)  43    2     6
zeropage      SRE oper      47    2     3
absolute      SRE oper      4F    3     4
(indirect),Y  SRE (oper),Y  53    2     5*
zeropage,X    SRE oper,X    57    2     4
absolute,Y    SRE oper,Y    5B    3     4*
absolute,X    SRE oper,X    5F    3     4*
'''

for generated in generate_classes_from_string(Sre, sre_types):
    types.append(generated)
