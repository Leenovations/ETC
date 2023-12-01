#!/usr/bin/python3

import sys
import argparse
import re
#-------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<IGV bed>', help='Set IGV bed file')
parser.add_argument('2', metavar='<Output>', help='Set output name')
args = parser.parse_args()
#-------------------------------------------------------------#
with open(sys.argv[2], 'w') as note:
    with open(sys.argv[1], 'r') as bed:
        for line in bed:
            line = line.strip()
            line = line.replace('chr', 'hs')
            splitted = re.split(r'[-\s;:]', line)
            joined = '\t'.join(splitted)

            note.write(joined + '\n')