import argparse

from cpu import CPU
from graphics.graphics import Window
from nes_test import NesTestLog
from ram import RAM
from apu import APU
from ppu import PPU
from rom import ROM


class Nes:
    def __init__(self, rom_bytes, testing):
        self.rom = ROM(rom_bytes)

        # create ram
        self.ram = RAM()

        # create ppu and apu
        self.ppu = PPU()
        self.apu = APU()

        # create cpu
        self.cpu = CPU(self.ram, self.ppu, self.apu)

        # create ppu window
        self.window = Window()

        self.testing = testing

        self.nes_test_log = None

    def load(self):
        self.cpu.start_up()
        self.cpu.load_rom(self.rom, self.testing)

        if self.testing:
            # load in the nes_test.log
            with open('nes_test.log', 'r') as nes_test_file:
                self.nes_test_log = NesTestLog(nes_test_file.readlines())

    def run(self):
        # load in the nes_test.log
        while True:
            self.update()
            self.draw()

    def update(self):
        self.cpu.identify()
        if self.testing:
            self.nes_test_log.compare(self.cpu)
        self.cpu.execute()

        self.window.update()

    def draw(self):
        self.window.draw()


def main():
    # set up command line argument parser
    parser = argparse.ArgumentParser(description='NES Emulator.')
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='path to nes rom')
    parser.add_argument('--test')
    args = parser.parse_args()

    # load rom
    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

    nes = Nes(rom_bytes, args.test)
    nes.load()
    nes.run()


if __name__ == '__main__':
    main()
