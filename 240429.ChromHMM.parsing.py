import gzip
#----------------------------------------------------------------------------------#
with open('/media/src/hg19/08.bed/K562HMM.tsv', 'w') as note01:
    with open('/media/src/hg19/08.bed/wgEncodeBroadHmmK562HMM.bed', 'r') as bed:
        for line in bed:
            line = line.strip()
            splitted = line.split('\t')
            Chr = splitted[0][3:]
            Start = splitted[1]
            End = splitted[2]
            Region = '_'.join(splitted[3].split('_')[1:])

            New_line = '\t'.join([Chr, Start, End, '*', '.', '.', Region + '\n'])
            note01.write(New_line)