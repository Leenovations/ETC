import glob
import pandas as pd
#--------------------------------------------------------#

TSV = glob.glob('/labmed/11.AML/03.GeneSet/*')
TSV.sort()

for tsv in TSV:
    pathway = tsv.split('/')[-1]
    pathway = pathway.split('.')[0]
    Data = pd.read_csv(tsv,
                       sep='\t')
    Gene_list = Data.iloc[16,1].split(',')

    Gene_dataframe = pd.DataFrame({'Gene' : Gene_list})
    Gene_dataframe.to_csv(f"{pathway}.Gene.List.txt",
                          sep='\t',
                          index=False)
    