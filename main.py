import argparse

from cpu import CPU
from rom import ROM


def main():
    # set up command line argument parser
    parser = argparse.ArgumentParser(description='NES Emulator.')
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='path to nes rom')
    args = parser.parse_args()

    # load rom
    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

    rom = ROM(rom_bytes)

    # create cpu
    cpu = CPU()
    cpu.run_rom(rom)

if __name__ == '__main__':
    main()
