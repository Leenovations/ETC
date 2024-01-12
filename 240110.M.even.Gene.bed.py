#!/home/lab/anaconda3/envs/NGS/bin/python3

import sys
import argparse
#--------------------------------------------------------------------#
parser = argparse.ArgumentParser(description="Pipeline Usage")
parser.add_argument('1', metavar='<window size>', help='Set window size')
args = parser.parse_args()
#--------------------------------------------------------------------#
GENE = {}
with open('/media/src/hg19/08.bed/whole.exome.gene.bed', 'r') as txt:
    for line in txt:
        line = line.strip()
        splitted = line.split('\t')
        Chr = splitted[0]
        Start = splitted[1]
        End = splitted[2]
        Gene = splitted[3]
        
        if Chr != 'M' and Chr != 'chrM':
            GENE[Gene] = Chr + '\t' + Start + '\t' + End
#--------------------------------------------------------------------#
with open(f"/media/src/hg19/01.Methylation/00.Bed/whole.exome.gene.{str(sys.argv[1])}bp.bed", 'w') as note:
    for gene in GENE.keys():
        Chr = GENE[gene].split('\t')[0]
        Start = int(GENE[gene].split('\t')[1])
        End = Start + int(sys.argv[1])
        note.write(Chr + '\t' + str(Start) + '\t' + str(End) + '\t' + gene + '\n')
        End_point = int(GENE[gene].split('\t')[2])
        while End_point > End :
            Start = End + 1
            End += int(sys.argv[1]) + 1

            if End >= End_point:
                note.write(Chr + '\t' + str(Start) + '\t' + str(End_point) + '\t' + gene + '\n')
                break
            else:
                note.write(Chr + '\t' + str(Start) + '\t' + str(End) + '\t' + gene + '\n')
#--------------------------------------------------------------------#
# with open(f"/media/src/hg19/01.Methylation/00.Bed/whole.exome.gene.{str(sys.argv[1])}bp.bed", 'r') as bed:
#     with open(f"/media/src/hg19/01.Methylation/00.Bed/whole.exome.gene.{str(sys.argv[1])}bp.Chr.bed", 'w') as note:
#         for line in bed:
#             line = line.replace('chr', '')
#             note.write(line)
# #--------------------------------------------------------------------#