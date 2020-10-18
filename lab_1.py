import os
import sys
import stat
import argparse

from elftools.elf.elffile import ELFFile


def parse_args():
    parser = argparse.ArgumentParser(
        description='Parse ELF file and output code section (if any).')
    parser.add_argument('filename', help='ELF file to process')
    return parser.parse_args()


def process_file(filename):
    print('Processing file:', filename)
    if not os.path.exists(filename):
        print(f'Error: There is not such file: {filename}')
        sys.exit(1)
    st = os.stat(filename)
    if not bool(st.st_mode & stat.S_IRGRP):
        print('Error: file is not readable')
        sys.exit(2)
    with open(filename, 'rb') as f:
        for sect in ELFFile(f).iter_sections():
            if sect.name != '.text':
                continue
            print('Section name:', sect.name)
            print('Section offset:', sect.header['sh_offset'])
            print('Section size:', sect.header['sh_size'])
            return
        print(f'There is no code section in {filename}')


if __name__ == '__main__':
    args = parse_args()
    process_file(args.filename)
