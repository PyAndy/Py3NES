from typing import List

import numpy as np

from instructions.generic_instructions import Instruction

from memory_owner import MemoryOwnerMixin
from ppu import PPU
from ram import RAM
from rom import ROM
from status import Status

import instructions.instructions as i_file
import instructions.jump_instructions as j_file
import instructions.load_instructions as l_file
import instructions.store_instructions as s_file
import instructions.bit_instructions as b_file
import instructions.arithmetic_instructions as a_file



class CPU(object):
    def __init__(self, ram: RAM, ppu: PPU):
        self.ram = ram
        self.ppu = ppu
        self.rom = None

        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu
        ]

        # instruction to execute
        self.instruction = None
        self.data_bytes = None

        # status registers: store a single byte
        self.status_reg = None  # type: Status

        # counter registers: store a single byte
        self.pc_reg = None  # program counter, 2 byte
        self.sp_reg = None  # stack pointer

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # program counter stores current execution point
        self.running = True

        # create the instructions that the cpu can interpret
        instructions_list = self._find_instructions(Instruction)
        self.instructions = {}
        for instruction in instructions_list:
            if instruction in self.instructions:
                raise Exception('Duplicate instruction identifier bytes')
            self.instructions[instruction.identifier_byte] = instruction

    def _find_instructions(self, cls):
        """
        finds all available instructions
        """
        subclasses = [subc for subc in cls.__subclasses__() if subc.identifier_byte is not None]
        return subclasses + [g for s in cls.__subclasses__() for g in self._find_instructions(s)]

    def start_up(self):
        """
        set the initial values of cpu registers
        status reg: 000100 (irqs disabled)
        x, y, a regs: 0
        stack pointer: $FD
        $4017: 0 (frame irq disabled)
        $4015: 0 (sound channels disabled)
        $4000-$400F: 0 (sound registers)
        """
        # TODO Hex vs binary
        self.pc_reg = 0  # 2 byte
        self.status_reg = Status()
        self.sp_reg = np.uint8(0xFD)

        self.x_reg = np.uint8(0)
        self.y_reg = np.uint8(0)
        self.a_reg = np.uint8(0)

        # TODO implement memory sets

    def get_memory(self, location: int, num_bytes: int=1) -> int:
        """
        returns a byte from a given memory location
        """
        memory_owner = self._get_memory_owner(location)
        return memory_owner.get(location, num_bytes)

    def _get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        """
        return the owner of a memory location
        """
        # check if memory owner
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def set_memory(self, location: int, value: int, num_bytes: int=1):
        """
        sets the memory at a location to a value
        """
        memory_owner = self._get_memory_owner(location)
        memory_owner.set(location, value, num_bytes)

    def increase_stack_size(self, size: int):
        """
        increases stack size by decreasing the stack pointer
        """
        self.sp_reg -= np.uint8(size)

    def decrease_stack_size(self, size: int):
        """
        decreases stack size by increasing the stack pointer
        """
        self.sp_reg += np.uint8(size)

    def load_rom(self, rom: ROM):
        # unload old rom
        if self.rom is not None:
            self.memory_owners.remove(self.rom)

        # load rom
        self.rom = rom
        self.pc_reg = 0xC000

        # load the rom program instructions into memory
        self.memory_owners.append(self.rom)

    def identify(self):
        # get the current byte at pc
        identifier_byte = self._get_memory_owner(self.pc_reg).get(self.pc_reg)

        # turn the byte into an Instruction
        self.instruction = self.instructions.get(identifier_byte, None)  # type: Instruction
        if self.instruction is None:
            raise Exception('Instruction not found: {}'.format(identifier_byte.hex()))

        # get the data bytes
        self.data_bytes = self.rom.get(self.pc_reg + 1, self.instruction.data_length)

        # print out diagnostic information
        # example: C000  4C F5 C5  JMP $C5F5                       A:00 X:00 Y:00 P:24 SP:FD CYC:  0
        print('{}, {}, {}, A:{}, X:{}, Y:{}, P:{}, SP:{}'.format(hex(self.pc_reg),
                                                                 (identifier_byte + self.data_bytes).hex(),
                                                                 self.instruction.__name__, self.a_reg, self.x_reg,
                                                                 self.y_reg, hex(self.status_reg.to_int()),
                                                                 hex(self.sp_reg)))

    def execute(self):

        # increment the pc_reg
        self.pc_reg += self.instruction.get_instruction_length()

        # we have a valid instruction class
        value = self.instruction.execute(self, self.data_bytes)

        self.status_reg.update(self.instruction, value)
