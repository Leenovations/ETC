#!/usr/bin/python3

import pandas as pd
import sys
import argparse
import glob
import os
#------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Code Usage')
parser.add_argument('1', metavar='<Path>', help='Set Path')
parser.add_argument('2', metavar='<Gene list>', help='Set Gene list file')
args = parser.parse_args()
#------------------------------------------------------------#
Gene = pd.read_csv(sys.argv[2],
                   sep='\t',
                   header=None)
#------------------------------------------------------------#
Files = glob.glob(f'{sys.argv[1]}/*tsv')
Files.sort()
#------------------------------------------------------------#
if os.path.isdir('01.Filtered'):
    pass
else:
    command = 'mkdir 01.Filtered'
    os.system(command)
#------------------------------------------------------------#
def Filter(sv):
    Name = sv.split('/')[-1]
    Name = Name.split('.')[0]
    Name = Name + '.structural.flt.results.xlsx'

    SV = pd.read_csv(sv,
                     sep='\t',
                     header='infer')
    
    SV_filtered = SV[SV['Gene1'].isin(Gene.iloc[:,0].tolist()) | SV['Gene2'].isin(Gene.iloc[:,0].tolist())]
    SV_filtered.insert(0, 'Result', '')
    SV_filtered.to_excel(f'01.Filtered/{Name}',
                       header='infer',
                       index=False)
    
list(map(Filter, Files))