#!/usr/bin/python3

import os
import sys
#-------------------------------------------------------------------------#
command = 'mkdir 00.RawData'
os.system(command)
#-------------------------------------------------------------------------#
with open('SRA.list.txt', 'r') as sra:
    for line in sra:
        line = line.strip()
        
        command = f'mkdir -p 00.RawData/{line}'
        os.system(command)

        with open(f'00.RawData/{line}/job.sh', 'w') as note:
            note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                       '#SBATCH -J SRA_Download' + '\n' + \
                       '#SBATCH -o Log.%j.out' + '\n' + \
                       f'#SBATCH --nodelist={sys.argv[1]}' + '\n' + \
                       '#SBATCH -n 1' + '\n' + '\n' + \
                       f'fastq-dump --split-3 -gzip --outdir ../ {line}')

with open('Total.Run.sh', 'w') as note:
    with open('SRA.list.txt', 'r') as sra:
        for line in sra:
            line = line.strip()

            Path = os.getcwd()
            note.write(f'cd {Path}/00.RawData/{line}; sbatch job.sh' + '\n'
