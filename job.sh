#!/bin/bash
#
#SBATCH -J XML
#SBATCH -o Log.%j.out
#SBATCH --time=UNLIMITED
#SBATCH --nodelist=node02
#SBATCH -n 2

python 240411.XML.streaming.parsing.py
