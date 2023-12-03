#!/usr/bin/python3

import os
import sys
import argparse
import glob
import time
import subprocess
#-------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<Tool>', help='Select download tool')
parser.add_argument('2', metavar='<node>', help='Select node')
parser.add_argument('3', metavar='<Max>', help='Set Max CPU or Not')
parser.add_argument('4', metavar='<SRA num>', nargs='+', help='Set SRA number')
args=parser.parse_args()
#-------------------------------------------------------------------------#
if os.path.isdir('00.RawData'):
    pass
else:
    command = 'mkdir 00.RawData'
    os.system(command)
#-------------------------------------------------------------------------#
SRA_list = sys.argv[4:]
#-------------------------------------------------------------------------#
def CPU_MAX():
    MAX_CPU = int(sys.argv[3])
    Allocated_CPU = 0
    PID_exe = []

    if sys.argv[1] == 'fasterq-dump':
        for sra in SRA_list:
            Allocated_CPU += 2

            command = f'mkdir -p 00.RawData/{sra}'
            os.system(command)

            with open(f'00.RawData/{sra}/job.sh', 'w') as note:
                note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                            '#SBATCH -J fasterq_dump' + '\n' + \
                            f'#SBATCH -o 00.RawData/{sra}/Log.%j.out' + '\n' + \
                            '#SBATCH --time=UNLIMITED' + '\n' + \
                            f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                            '#SBATCH -n 2' + '\n' + '\n' + \
                            f'fasterq-dump -S -t 00.RawData/{sra}/TEMP/ -e 8 -m 5000MB -O ../ {sra}')
            
            command = f'sbatch 00.RawData/{sra}/job.sh'
            os.system(command)

            time.sleep(3)

            JobID = glob.glob(f'00.RawData/{sra}/Log*')
            JobID.sort(reverse=True)
            JobID = [s.replace(f'00.RawData/{sra}/', '') for s in JobID][0]
            JobID = JobID.split('.')[1]

            Pid = subprocess.check_output(f"scontrol listpids | column -t | grep {JobID} | head -n 1 | awk '{{print $1}}'", shell=True, text=True).strip()
            PID_exe.append(int(Pid))
            print(PID_exe)

            if MAX_CPU < Allocated_CPU:
                break
        
        Scheduled_SRA = SRA_list[len(PID_exe) + 1 : ]
        print(Scheduled_SRA)

def CPU_free():
    if sys.argv[1] == 'fasterq-dump':
        for sra in SRA_list:
            command = f'mkdir -p 00.RawData/{sra}'
            os.system(command)

            with open(f'00.RawData/{sra}/job.sh', 'w') as note:
                note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                            '#SBATCH -J fasterq_dump' + '\n' + \
                            '#SBATCH -o Log.%j.out' + '\n' + \
                            '#SBATCH --time=UNLIMITED' + '\n' + \
                            f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                            '#SBATCH -n 2' + '\n' + '\n' + \
                            f'fasterq-dump -S -t TEMP/ -e 8 -m 5000MB -O ../ {sra}')

        with open('Total.Run.sh', 'w') as note:
            for sra in SRA_list:
                Path = os.getcwd()
                note.write(f'cd {Path}/00.RawData/{sra}; sbatch job.sh' + '\n')

    elif sys.argv[1] == 'fastq-dump':
        for sra in SRA_list:
            command = f'mkdir -p 00.RawData/{sra}'
            os.system(command)

            with open(f'00.RawData/{sra}/job.sh', 'w') as note:
                note.write('#!/bin/bash' + '\n' + '#' + '\n' + \
                            '#SBATCH -J fastq_dump' + '\n' + \
                            '#SBATCH -o Log.%j.out' + '\n' + \
                            '#SBATCH --time=UNLIMITED' + '\n' + \
                            f'#SBATCH --nodelist={sys.argv[2]}' + '\n' + \
                            '#SBATCH -n 2' + '\n' + '\n' + \
                            f'fastq-dump --split-files -gzip --outdir ../ {sra}')

        with open('Total.Run.sh', 'w') as note:
            for sra in SRA_list:
                Path = os.getcwd()
                note.write(f'cd {Path}/00.RawData/{sra}; sbatch job.sh' + '\n')

if sys.argv[3] != 'None':
    CPU_MAX()
elif sys.argv[3] == 'None':
    CPU_free()