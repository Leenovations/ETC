#!/home/lab/anaconda3/envs/NGS/bin/python3

import pandas as pd
#------------------------------------------------------------#
with open("/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Exon.Chr.X.bed", "r") as bed:
    with open("/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.GeneCNV.Chr.X.bed", "w") as note:
        for line in bed:
            line = line.strip()
            splitted = line.split('\t')
            Chr = splitted[0]
            Start = int(splitted[1])
            End = int(splitted[2])
            Gene = splitted[3]
            Exon = splitted[4]
            Strand = splitted[5]

            for position in range(Start, End + 1):
                note.write(Chr + str(position) + '\t' + str(position) + '\t' + Gene + '\t' + Exon + '\t' + Strand + '\n')