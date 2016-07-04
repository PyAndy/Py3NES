from typing import List

import numpy as np

from instructions.generic_instructions import Instruction

from memory_owner import MemoryOwnerMixin
from ppu import PPU
from apu import APU
from ram import RAM
from rom import ROM
from status import Status

import instructions.instructions as i_file
import instructions.jump_instructions as j_file
import instructions.load_instructions as l_file
import instructions.store_instructions as s_file
import instructions.bit_instructions as b_file
import instructions.arithmetic_instructions as a_file
import instructions.combination_instructions as c_file


class CPU(object):
    def __init__(self, ram: RAM, ppu: PPU, apu: APU):
        self.ram = ram
        self.ppu = ppu
        self.apu = apu
        self.rom = None

        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu,
            self.apu
        ]

        # instruction to execute
        self.instruction = None
        self.data_bytes = None
        self.instruction_byte = None

        # status registers: store a single byte
        self.status_reg = None  # type: Status

        # counter registers: store a single byte
        self.pc_reg = None  # program counter, 2 byte
        self.sp_reg = None  # stack pointer
        self.stack_offset = 0x100

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
            if instruction.identifier_byte in self.instructions.keys():
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
        self.pc_reg = np.uint16(0)  # 2 byte
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

    def set_stack_value(self, value: int, num_bytes: int):
        """
        sets a value on the stack, and decrements the stack pointer
        """
        # store the value on the stack
        self.set_memory(self.stack_offset + self.sp_reg, value, num_bytes=num_bytes)

        # increases the size of the stack
        self.sp_reg -= np.uint8(num_bytes)

    def get_stack_value(self, num_bytes: int):
        """
        gets a value on the stack, and increments the stack pointer
        """
        # decrease the size of the stack
        self.sp_reg += np.uint8(num_bytes)

        # grab the stored value from the stack
        return self.get_memory(self.stack_offset + self.sp_reg, num_bytes=num_bytes)

    def load_rom(self, rom: ROM, testing):
        # unload old rom
        if self.rom is not None:
            self.memory_owners.remove(self.rom)

        # load rom
        self.rom = rom

        # load the rom program instructions into memory
        self.memory_owners.append(self.rom)

        if testing:
            self.pc_reg = np.uint16(0xC000)
        else:
            self.pc_reg = np.uint16(int.from_bytes(self.get_memory(0xFFFC, 2), byteorder='little'))

    def identify(self):
        # get the current byte at pc
        rom_instruction = True
        self.instruction_byte = self._get_memory_owner(self.pc_reg).get(self.pc_reg)
        if type(self.instruction_byte) is not bytes:
            rom_instruction = False
            self.instruction_byte = bytes([self.instruction_byte])

        # turn the byte into an Instruction
        self.instruction = self.instructions.get(self.instruction_byte, None)  # type: Instruction
        if self.instruction is None:
            raise Exception('Instruction not found: {}'.format(self.instruction_byte.hex()))

        # get the data bytes
        if rom_instruction:
            self.data_bytes = self.rom.get(self.pc_reg + np.uint16(1), self.instruction.data_length)
        else:
            if self.instruction.data_length > 0:
                self.data_bytes = bytes([self.get_memory(self.pc_reg + np.uint16(1), self.instruction.data_length)])
            else:
                self.data_bytes = bytes()

        # print out diagnostic information
        # example: C000  4C F5 C5  JMP $C5F5                       A:00 X:00 Y:00 P:24 SP:FD CYC:  0
        print('{}, {}, {}, A:{}, X:{}, Y:{}, P:{}, SP:{}'.format(hex(self.pc_reg),
                                                                 (self.instruction_byte + self.data_bytes).hex(),
                                                                 self.instruction.__name__, hex(self.a_reg),
                                                                 hex(self.x_reg), hex(self.y_reg),
                                                                 hex(self.status_reg.to_int()), hex(self.sp_reg)))

    def execute(self):

        # increment the pc_reg
        self.pc_reg += np.uint16(self.instruction.get_instruction_length())

        # we have a valid instruction class
        value = self.instruction.execute(self, self.data_bytes)

        self.status_reg.update(self.instruction, value)
