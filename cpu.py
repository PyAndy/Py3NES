from collections import defaultdict
from typing import List

from instruction import LdaImmInstruction, SeiInstruction, CldInstruction, StaAbsInstruction
from memory_owner import MemoryOwnerMixin
from ram import RAM
from ppu import PPU
from rom import ROM
from status import Status


class CPU(object):
    def __init__(self, ram: RAM, ppu: PPU):
        self.ram = ram
        self.ppu = ppu
        self.rom = None

        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu
        ]

        # status registers: store a single byte
        self.status_reg = None  # type: Status

        # counter registers: store a single byte
        self.pc_reg = None  # program counter
        self.sp_reg = None  # stack pointer

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # program counter stores current execution point
        self.running = True

        self.instructions = [
            SeiInstruction(),
            CldInstruction(),
            LdaImmInstruction(),
            StaAbsInstruction()
        ]

        self.instructions_mapping = defaultdict()
        for instruction in self.instructions:
            self.instructions_mapping[instruction.identifier_byte] = instruction

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
        self.pc_reg = 0
        self.status_reg = Status()
        self.sp_reg = 0xFD

        self.x_reg = 0
        self.y_reg = 0
        self.a_reg = 0

        # TODO implement memory sets

    def get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        """
        return the owner of a memory location
        """
        # check if rom
        if self.rom.memory_start_location <= location <= self.rom.memory_end_location:
                return self.rom

        # check if memory owner
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def run_rom(self, rom: ROM):
        # load rom
        self.rom = rom
        self.pc_reg = self.rom.header_size

        # run program
        self.running = True
        while self.running:
            # get the current byte at pc
            identifier_byte = self.rom.get(self.pc_reg)

            # turn the byte into an Instruction
            instruction = self.instructions_mapping.get(identifier_byte, None)
            if instruction is None:
                raise Exception('Instruction not found: {}'.format(identifier_byte))

            # get the correct amount of data bytes
            num_data_bytes = instruction.instruction_length - 1

            # get the data bytes
            data_bytes = self.rom.get(self.pc_reg + 1, num_data_bytes)

            # we have a valid instruction class
            instruction.execute(self, data_bytes)

            self.pc_reg += instruction.instruction_length
