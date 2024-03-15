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
command = 'pwd'
Dir = os.getcwd()
#-----------------------------------------------------------------------------#
with open('SampleSheet.txt', 'r') as samplesheet:
    Sample_Count = 0
    Sample_Dir = []
    Sample_Name = []
    for line in samplesheet:
        Sample_name = line.split('\t')[0]
        Sample_Name.append(Sample_name)
        Sample_Count += 1
        Sample_Dir.append(Dir + '/' + Sample_name + '/')
    Sample_Dir = ','.join(Sample_Dir)
    Sample_Name = ','.join(Sample_Name)
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
if BATCH['Node'] == 'node01' and int(BATCH['CPU']) > 128:
    raise ValueError("\033[91mValueError: Total CPU is less than 128\033[0m")
elif BATCH['Node'] == 'node02' and int(BATCH['CPU']) > 56:
    raise ValueError("\033[91mValueError: Total CPU is less than 56\033[0m")
elif BATCH['Node'] == 'node03' and int(BATCH['CPU']) > 32:
    raise ValueError("\033[91mValueError: Total CPU is less than 32\033[0m")
elif BATCH['Node'] == 'node04' and int(BATCH['CPU']) > 28:
    raise ValueError("\033[91mValueError: Total CPU is less than 28\033[0m")
#-----------------------------------------------------------------------------#
if {BATCH['Node']} == 'node04':
    Cpu = int(BATCH['CPU'])
    Allocated_CPU = int(Cpu / Sample_Count)
    CPU = [Allocated_CPU] * Sample_Count
elif {BATCH['Node']} != 'node04':
    Cpu = int(BATCH['CPU'])
    Allocated_CPU = int(Cpu / Sample_Count)
    if Allocated_CPU < 2:
        raise ValueError("\033[91m" + "ValueError: Allocated CPU is less than 2" + "\033[0m")
    elif Allocated_CPU >= 2:
        if Allocated_CPU % 2 == 0:
            if int(Cpu % Sample_Count) < 2:
                CPU = [Allocated_CPU] * Sample_Count
            elif int(Cpu % Sample_Count) >= 2:
                CPU = [Allocated_CPU] * Sample_Count
                How_many = int((Cpu % Sample_Count) / 2) #분배를 2씩 해주는 경우 -> 용량에 따라 나누어야함
                for idx in range(0, How_many):
                    CPU[idx] = CPU[idx] + 2
        elif Allocated_CPU % 2 == 1:
            CPU = [Allocated_CPU - 1] * Sample_Count
            Rest_CPU = Sample_Count + Allocated_CPU % Sample_Count - 1
            How_many = int(Rest_CPU / 2) #분배를 2씩 해주는 경우 -> 용량에 따라 나누어야함
            for idx in range(0, How_many):
                CPU[idx] = CPU[idx] + 2
#-----------------------------------------------------------------------------#        
if BATCH['Run.type'] == 'WGS':
    Code = '/labmed/00.Code/Pipeline/WGS.py'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
elif BATCH['Run.type'] == 'WES':
    Code = '/labmed/00.Code/Pipeline/WES.py'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
elif BATCH['Run.type'] == 'WGBS':
    Code = '/labmed/00.Code/Pipeline/WGBS.py'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
        os.system(command)
elif BATCH['Run.type'] == 'RNA':
    Code = '/labmed/00.Code/Pipeline/RNASeq.py'
    if os.path.isdir("Genecount"):
        pass
    else:
        command = "mkdir -p Genecount/"
        os.system(command)
elif BATCH['Run.type'] == 'Gleevec':
    Code = '/labmed/01.Pipeline/230804.Imatinib.comp.py'
    if os.path.isdir("Results"):
        pass
    else:
        command = "mkdir -p Results/"
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
        BATCH['Sample.Name'] = Sample_Name
        BATCH['Sample.Dir'] = Sample_Dir
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
with open('Total.Run.sh', 'w') as note:
    with open('SampleSheet.txt', 'r') as samp:
        Sample_Count = 0
        for line in samp:
            line = line.strip()
            splitted = line.split('\t')
            Name = str(splitted[0])

            note.write('cd ' + Dir + '/' + Name + '; ' + 'sbatch job.sh' + '\n')
#-----------------------------------------------------------------------------#