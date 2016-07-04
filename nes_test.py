from typing import List
import re

from cpu import CPU


class NesTestLog:
    def __init__(self, lines: List[str]):
        self.lines = []  # type: List[NesTestLine]
        self.index = 0

        pattern = r'(.{4})\s*(.{9}).(.{4})(.{28})A:(.{2})\sX:(.{2})\sY:(.{2})\sP:(.{2})\sSP:(.{2})\sCYC:(.*)'
        compiled = re.compile(pattern)
        for line in lines:
            self.lines.append(NesTestLine(line, compiled))

    def compare(self, cpu: CPU):
        self.lines[self.index].compare(cpu)

        self.index += 1


class NesTestLine:
    """
    PC Bytes Instruction A X Y P SP CYC
    C000  4C F5 C5  JMP $C5F5                       A:00 X:00 Y:00 P:24 SP:FD CYC:  0
    """
    def __init__(self, line: str, compiled_pattern):
        self.line = line

        matches = compiled_pattern.match(self.line)

        self.expected_pc_reg = int(matches.group(1), 16)
        expected_data = matches.group(2)[3:].strip()
        if expected_data:
            self.expected_bytes = bytes([int(x, 16) for x in expected_data.split(' ')])
        else:
            self.expected_bytes = bytes()
        self.expected_instruction = matches.group(3).strip()
        self.expected_instruction_data = matches.group(4).strip()

        self.expected_a = int(matches.group(5), 16)
        self.expected_x = int(matches.group(6), 16)
        self.expected_y = int(matches.group(7), 16)
        self.expected_p = int(matches.group(8), 16)
        self.expected_sp = int(matches.group(9), 16)
        self.expected_cyc = int(matches.group(10))

    def compare(self, cpu: CPU) -> bool:
        """
        checks a cpu against a log line
        """
        pc_match = self.expected_pc_reg == cpu.pc_reg
        instruction_match = self.expected_instruction in cpu.instruction.__name__.upper()
        data_bytes_match = self.expected_bytes == cpu.data_bytes
        a_match = self.expected_a == cpu.a_reg
        x_match = self.expected_x == cpu.x_reg
        y_match = self.expected_y == cpu.y_reg
        p_match = self.expected_p == cpu.status_reg.to_int()
        sp_match = self.expected_sp == cpu.sp_reg
        valid = pc_match and instruction_match and a_match and x_match and y_match and p_match and sp_match and data_bytes_match
        if not valid:
            raise Exception('Instruction results not expected\n{}'.format(cpu.instruction))
