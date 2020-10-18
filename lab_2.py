import os
import sys
import stat
import argparse
from collections import defaultdict

from elftools.elf.elffile import ELFFile


def parse_args():
    parser = argparse.ArgumentParser(
        description='Parse ELF file and output code section (if any).')
    parser.add_argument('filename', help='ELF file to process')
    return parser.parse_args()


def print_bytes_section(section):
    bytes_count = defaultdict(int)
    max_count = 0
    for section_byte in section.data():
        bytes_count[section_byte] += 1
        max_count = max(max_count, bytes_count[section_byte])
    print('Bytes:')
    for byte_int, count in sorted(
            bytes_count.items(), key=lambda item: item[0]):
        sticks = '|' * max(1, int((count / max_count) * 60))
        byte_str = f'{byte_int:x}'
        print(f'{byte_str:>2} {count:>4}   {sticks}')


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
            print_bytes_section(sect)
            return
        print(f'There is no code section in {filename}')


if __name__ == '__main__':
    args = parse_args()
    process_file(args.filename)
