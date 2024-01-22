import pandas as pd
import numpy as np
import pyranges as pr
import glob
#----------------------------------------------------------------------------------------#
Data = pd.read_csv('/labmed/11.AML/240119.AML.150bp.Methyl.txt',
                    sep='\t',
                    header='infer')
pyData = pr.PyRanges(Data)
#----------------------------------------------------------------------------------------#
Gene = pd.read_csv('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.±.5kb.Gene.bed',
                   sep='\t',
                   names = ['Chromosome', 'Start', 'End' ,'GeneSymbol', 'Strand'])
pyGene = pr.PyRanges(Gene)
#----------------------------------------------------------------------------------------#
Promoter = pd.read_csv('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Promoter.bed',
                   sep='\t',
                   names = ['Chromosome', 'Start', 'End' ,'GeneSymbol', 'Region', 'Strand'])
pyPromoter = pr.PyRanges(Promoter)
#----------------------------------------------------------------------------------------#
Exon = pd.read_csv('/media/src/hg19/01.Methylation/00.Bed/NCBI.RefSeq.Selected.Exon.Intron.bed',
                   sep='\t',
                   names = ['Chromosome', 'Start', 'End' ,'GeneSymbol', 'Region', 'Strand'])
pyExon = pr.PyRanges(Exon)
#----------------------------------------------------------------------------------------#
CpG = pd.read_csv('/media/src/hg19/01.Methylation/00.Bed/CpG.Island.bed',
                   sep='\t',
                   names = ['Chromosome', 'Start', 'End' ,'GeneSymbol', 'Region', 'Strand'])
CpG_Island = CpG[CpG['Region'] == 'CpG_Island']
pyIsland = pr.PyRanges(CpG_Island)

CpG_Shore = CpG[CpG['Region'] == 'CpG_Shore']
pyShore = pr.PyRanges(CpG_Shore)

CpG_Shelf = CpG[CpG['Region'] == 'CpG_Shelf']
pyShelf = pr.PyRanges(CpG_Shelf)
#----------------------------------------------------------------------------------------#
Enhancer = pd.read_csv('/media/src/hg19/01.Methylation/00.Bed/Inhancer.anno.bed',
                   sep='\t',
                   names = ['Chromosome', 'Start', 'End' ,'GeneSymbol', 'Region', 'Strand'])
pyEnhancer = pr.PyRanges(Enhancer)
#----------------------------------------------------------------------------------------#
Pathway = glob.glob('/labmed/11.AML/03.GeneSet/*Gene.List.txt')
Pathway.sort()

for pathway in Pathway[0:1]:
    Pathway_name = pathway.split('/')[-1]
    Pathway_name = Pathway_name.replace('.Gene.List.txt', '')
    GeneList = pd.read_csv(pathway, sep='\t', header='infer')

    PROMOTER = []
    EXON = []
    INTRON = []
    CPGISLAND = []
    CPGSHORE = []
    CPGSHELF = []
    ENHANCER = []

    for gene in GeneList['Gene'].to_list():
        Gene_Range = Gene[(Gene['GeneSymbol'] == gene) & (Gene['Chromosome'].str.contains('_') == False)]
        pyGene_Range = pr.PyRanges(Gene_Range)
        #-----------------------------------------------------------------------------------------------------------------------------------#
        Intersect = pyIsland.join(pyGene_Range, apply_strand_suffix=False).df
        if not pd.DataFrame(Intersect).empty:
            Intersect = Intersect.drop(['Start_b', 'End_b', 'Strand_b'], axis=1)
            Intersect = pr.PyRanges(Intersect)
            Intersect = Intersect.join(pyData).df
            if not pd.DataFrame(Intersect).empty:
                Intersect = Intersect.drop(['Start', 'End', 'GeneSymbol', 'Start_b', 'End_b'], axis=1)
                Intersect = round(Intersect.groupby(['Chromosome']).mean(), 3)
                Intersect = Intersect.reset_index()
                CPGISLAND.append(Intersect)
        #-----------------------------------------------------------------------------------------------------------------------------------#
        Intersect = pyShore.join(pyGene_Range, apply_strand_suffix=False).df
        if not pd.DataFrame(Intersect).empty:
            Intersect = Intersect.drop(['Start_b', 'End_b', 'Strand_b'], axis=1)
            Intersect = pr.PyRanges(Intersect)
            Intersect = Intersect.join(pyData).df
            if not pd.DataFrame(Intersect).empty:
                Intersect = Intersect.drop(['Start', 'End', 'GeneSymbol', 'Start_b', 'End_b'], axis=1)
                Intersect = round(Intersect.groupby(['Chromosome']).mean(), 3)
                Intersect = Intersect.reset_index()
                CPGSHORE.append(Intersect)
        #-----------------------------------------------------------------------------------------------------------------------------------#
        Intersect = pyShelf.join(pyGene_Range, apply_strand_suffix=False).df
        if not pd.DataFrame(Intersect).empty:
            Intersect = Intersect.drop(['Start_b', 'End_b', 'Strand_b'], axis=1)
            Intersect = pr.PyRanges(Intersect)
            Intersect = Intersect.join(pyData).df
            if not pd.DataFrame(Intersect).empty:
                Intersect = Intersect.drop(['Start', 'End', 'GeneSymbol', 'Start_b', 'End_b'], axis=1)
                Intersect = round(Intersect.groupby(['Chromosome']).mean(), 3)
                Intersect = Intersect.reset_index()
                CPGSHELF.append(Intersect)
        #-----------------------------------------------------------------------------------------------------------------------------------#
        Intersect = pyEnhancer.join(pyGene_Range, apply_strand_suffix=False).df
        if not pd.DataFrame(Intersect).empty:
            Intersect = Intersect.drop(['Start_b', 'End_b', 'Strand_b'], axis=1)
            Intersect = pr.PyRanges(Intersect)
            Intersect = Intersect.join(pyData).df
            if not pd.DataFrame(Intersect).empty:
                Intersect = Intersect.drop(['Start', 'End', 'GeneSymbol', 'Start_b', 'End_b'], axis=1)
                Intersect = round(Intersect.groupby(['Chromosome']).mean(), 3)
                Intersect = Intersect.reset_index()
                ENHANCER.append(Intersect)
        #-----------------------------------------------------------------------------------------------------------------------------------#
        Gene_Promoter = Promoter[(Promoter['GeneSymbol'] == gene) & (Promoter['Chromosome'].str.contains('_') == False)]
        pyGene_Promoter = pr.PyRanges(Gene_Promoter)

        Intersect = pyGene_Promoter.join(pyData).df
        Intersect = Intersect.drop(['Start', 'End', 'Start_b', 'End_b', 'Strand_b'], axis=1)
        Intersect = Intersect.astype({'Chromosome': 'str'})
        Intersect = round(Intersect.groupby(['Chromosome']).mean(), 3)
        Intersect = Intersect.fillna('NaN')
        PROMOTER.append(Intersect)
        #-----------------------------------------------------------------------------------------------------------------------------------#
        Gene_Exon = Exon[(Exon['GeneSymbol'] == gene) & (Exon['Chromosome'].str.contains('_') == False) & (Exon['Region'] == 'exon')]
        pyGene_Exon = pr.PyRanges(Gene_Exon)

        Intersect = pyGene_Exon.join(pyData).df
        Intersect = Intersect.drop(['Start', 'End', 'Start_b', 'End_b', 'Strand_b'], axis=1)
        Intersect = Intersect.astype({'Chromosome': 'str'})
        Intersect = round(Intersect.groupby(['Chromosome']).mean(), 3)
        Intersect = Intersect.fillna('NaN')
        EXON.append(Intersect)
        #-----------------------------------------------------------------------------------------------------------------------------------#
        Gene_Intron = Exon[(Exon['GeneSymbol'] == gene) & (Exon['Chromosome'].str.contains('_') == False) & (Exon['Region'] == 'intron')]
        pyGene_Intron = pr.PyRanges(Gene_Intron)

        Intersect = pyGene_Intron.join(pyData).df
        Intersect = Intersect.drop(['Start', 'End', 'Start_b', 'End_b', 'Strand_b'], axis=1)
        Intersect = Intersect.astype({'Chromosome': 'str'})
        Intersect = round(Intersect.groupby(['Chromosome']).mean(), 3)
        Intersect = Intersect.fillna('NaN')
        INTRON.append(Intersect)
        #-----------------------------------------------------------------------------------------------------------------------------------#