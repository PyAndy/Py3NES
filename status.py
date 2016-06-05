class Status:
    """
    7  bit  0
    ---- ----
    NVss DIZC
    |||| ||||
    |||| |||+- Carry: 1 if last addition or shift resulted in a carry, or if
    |||| |||     last subtraction resulted in no borrow
    |||| ||+-- Zero: 1 if last operation resulted in a 0 value
    |||| |+--- Interrupt: Interrupt inhibit
    |||| |       (0: /IRQ and /NMI get through; 1: only /NMI gets through)
    |||| +---- Decimal: 1 to make ADC and SBC use binary-coded decimal arithmetic
    ||||         (ignored on second-source 6502 like that in the NES)
    ||++------ s: No effect, used by the stack copy, see note below
    |+-------- Overflow: 1 if last ADC or SBC resulted in signed overflow,
    |            or D6 from last BIT
    +--------- Negative: Set to bit 7 of the last operation
    """
    def __init__(self):
        self.negative_bit = False  # type: bool
        self.overflow_bit = False  # type: bool
        self.interrupt_bit = True  # type: bool
        self.decimal_bit = False  # type: bool
        self.zero_bit = False  # type: bool
        self.carry_bit = False  # type: bool
