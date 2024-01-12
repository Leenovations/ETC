#!/usr/bin/python3
import sys
import os
import glob
import argparse
import pandas as pd
import numpy as np
#-----------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Pipeline Usage')
args = parser.parse_args()
#-----------------------------------------------------------------------------#
with open('SampleSheet.txt', 'r') as samplesheet:
    Sample_Count = 0
    for line in samplesheet:
        Sample_Count += 1
#-----------------------------------------------------------------------------#
BATCH = {}
with open('batch.config', 'r') as batch:
    for line in batch:
        line = line.strip()
        splitted = line.split('=')
        Key = splitted[0]
        Value = splitted[1]
        BATCH[Key] = Value
#-----------------------------------------------------------------------------#    
Cpu = int(BATCH['CPU'])
intervals = np.linspace(1, Cpu, Sample_Count + 1, dtype=int)
CPU = np.diff(intervals)
CPU = [cpu - 1 if cpu % 2 != 0 else cpu for cpu in CPU]
#-----------------------------------------------------------------------------#
if BATCH['Run.type'] == 'WGS':
    Code = '/labmed/00.Code/Pipeline/WGS.py'
    if os.path.isdir("Intermediate"):
        pass
    else:
        command = "mkdir -p Intermediate/"
        os.system(command)
elif BATCH['Run.type'] == 'WES':
    Code = '/labmed/00.Code/Pipeline/WES.py'
    if os.path.isdir("Intermediate"):
        pass
    else:
        command = "mkdir -p Intermediate/"
        os.system(command)
elif BATCH['Run.type'] == 'WGBS':
    Code = '/labmed/00.Code/Pipeline/WGBS.py'
    if os.path.isdir("Intermediate"):
        pass
    else:
        command = "mkdir -p Intermediate/"
        os.system(command)
elif BATCH['Run.type'] == 'mRNA':
    Code = '/labmed/00.Code/Pipeline/RNASeq.py'
    if os.path.isdir("Intermediate"):
        pass
    else:
        command = "mkdir -p Intermediate/"
        os.system(command)
elif BATCH['Run.type'] == 'Gleevec':
    Code = '/labmed/01.Pipeline/230804.Imatinib.comp.py'
    if os.path.isdir("Intermediate"):
        pass
    else:
        command = "mkdir -p Intermediate/"
        os.system(command)
#-----------------------------------------------------------------------------#
with open('SampleSheet.txt', 'r') as samplesheet:
    num = 0
    for line in samplesheet:
        line = line.strip()
        splitted = line.split('\t')
        Name = splitted[0]
        Cpu = CPU[num]
        BATCH['CPU'] = CPU[num]
        BATCH['SampleCount'] = Sample_Count
        with open(f'{Name}/{Name}.batch.config', 'w') as note:
            for Key in BATCH.keys():
                note.write(Key + '=' + str(BATCH[Key]) + '\n')

        with open(f'{Name}/job.sh', 'w') as note:
            note.write("#!/bin/bash" + '\n'
                        + "#" + '\n'
                        + f"#SBATCH -J {BATCH['Run.type']}" + '\n'
                        + f"#SBATCH -o Log.%j.out" + '\n'
                        + f"#SBATCH --time=UNLIMITED" + '\n'
                        + f"#SBATCH --nodelist={BATCH['Node']}" + '\n'
                        + f"#SBATCH -n {Cpu}" + '\n'
                        + '\n'
                        + f"python3 {Code}")
        num += 1
#-----------------------------------------------------------------------------#
command = 'pwd'
Dir = os.getcwd()

with open('Total.Run.sh', 'w') as note:
    with open('SampleSheet.txt', 'r') as samp:
        Sample_Count = 0
        for line in samp:
            line = line.strip()
            splitted = line.split('\t')
            Name = str(splitted[0])

            note.write('cd ' + Dir + '/' + Name + '; ' + 'sbatch job.sh' + '\n')
#-----------------------------------------------------------------------------#