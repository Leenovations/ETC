    # with open('/labmed/02.AML/test.tsv', 'r') as tsv:
with open('/media/src/hg19/08.bed/NCBI.RefSeq.All.Promoter.UTR.Exon.Intron.tsv', 'w') as note01:
    with open('/labmed/02.AML/NCBI.RefSeq.All.tsv', 'r') as tsv:
        for line in tsv:
            if line.startswith('#'):
                continue
            else:
                line = line.strip()
                splitted = line.split('\t')
                NM = splitted[0]
                Chr = splitted[1][3:]
                if '_' in Chr or Chr.startswith('MT'):
                    continue
                Strand = splitted[2]
                TxStart = splitted[3]
                TxEnd = splitted[4]
                CdsStart = splitted[5]
                CdsEnd = splitted[6]
                ExonCount = int(splitted[7])
                GeneSymbol = splitted[10]

                if Strand == '+':
                    Promoter_Start = str(int(TxStart) - 1 - 4000)
                    Promoter_End = str(int(TxStart) - 1)
                    
                    FiveUTR_Start = TxStart
                    FiveUTR_End = str(int(CdsStart) - 1)

                    ThreeUTR_Start = str(int(CdsEnd) + 1)
                    ThreeUTR_End = TxEnd

                    ExonStart = splitted[8].split(',')[0:ExonCount]
                    ExonEnd = splitted[9].split(',')[0:ExonCount]

                    Intron_Start = [str(int(Intron_start) + 1) for Intron_start in ExonEnd[:ExonCount - 1]]
                    Intron_End = [str(int(Intron_end) - 1) for Intron_end in ExonStart[1:ExonCount]]

                    note01.write(Chr + '\t' + Promoter_Start + '\t' + Promoter_End + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + 'Promoter' + '\n')
                    note01.write(Chr + '\t' + FiveUTR_Start + '\t' + FiveUTR_End + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + '5_UTR' + '\n')
                    for num in range(ExonCount):
                        if num == ExonCount - 1:
                            note01.write(Chr + '\t' + ExonStart[num] + '\t' + ExonEnd[num] + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + f'Exon_{str(num+1)}' + '\n')
                        else:
                            note01.write(Chr + '\t' + ExonStart[num] + '\t' + ExonEnd[num] + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + f'Exon_{str(num+1)}' + '\n')
                            note01.write(Chr + '\t' + Intron_Start[num] + '\t' + Intron_End[num] + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + f'Intron_{str(num+1)}' + '\n')
                    note01.write(Chr + '\t' + ThreeUTR_Start + '\t' + ThreeUTR_End + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + '3_UTR' + '\n')

                elif Strand == '-':
                    Promoter_Start = str(int(TxEnd) + 1 + 4000)
                    Promoter_End = str(int(TxEnd) + 1)
                    
                    FiveUTR_Start = TxEnd
                    FiveUTR_End = str(int(CdsEnd) + 1)

                    ThreeUTR_Start = str(int(CdsStart) - 1)
                    ThreeUTR_End = TxStart

                    ExonEnd = splitted[8].split(',')[0:ExonCount][::-1]
                    ExonStart = splitted[9].split(',')[0:ExonCount][::-1]

                    Intron_Start = [str(int(Intron_start) - 1) for Intron_start in ExonEnd[:ExonCount - 1]]
                    Intron_End = [str(int(Intron_end) + 1) for Intron_end in ExonStart[1:ExonCount]]

                    note01.write(Chr + '\t' + ThreeUTR_End + '\t' + ThreeUTR_Start + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + '3_UTR' + '\n')
                    for num in range(ExonCount)[::-1]:
                        if num == ExonCount - 1:
                            note01.write(Chr + '\t' + ExonEnd[num] + '\t' + ExonStart[num] + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + f'Exon_{str(num+1)}' + '\n')
                        else:
                            note01.write(Chr + '\t' + Intron_End[num] + '\t' + Intron_Start[num] + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + f'Intron_{str(num+1)}' + '\n')
                            note01.write(Chr + '\t' + ExonEnd[num] + '\t' + ExonStart[num] + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + f'Exon_{str(num+1)}' + '\n')
                    note01.write(Chr + '\t' + FiveUTR_End + '\t' + FiveUTR_Start + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + '5_UTR' + '\n')
                    note01.write(Chr + '\t' + Promoter_End + '\t' + Promoter_Start + '\t' + Strand + '\t' + GeneSymbol + '\t' + NM + '\t' + 'Promoter' + '\n')