#!/bin/bash
#
#SBATCH -J GeneCNV
#SBATCH -o Log.%j.out
#SBATCH --time=UNLIMITED
#SBATCH --nodelist=node01
#SBATCH -n 2

python3 240114.M.GeneCNV.Range.py
