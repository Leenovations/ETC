import pandas as pd
import re


AA = pd.read_csv('/media/src/Amino.Acid.txt', sep='\t', header=None,
                 names = ['full', 'alpha', 'abb'])
CONVERT = dict(zip(AA['alpha'].to_list(), AA['abb'].to_list()))
CONVERT.update({'X' : ''})
CONVERT.update({'Z' : 'E,Q'})

DRUG = {}
with open('ABL1.Drug.txt', 'r') as drug:
    for line in drug:
        line = line.strip()
        splitted = line.split('\t')
        if splitted[5] == 'Tyrosine kinase inhibitor - NS':
            splitted[5] = 'TKI'
        if splitted[9] == 'p.?':
            continue
        if splitted[9] not in DRUG:
            DRUG[splitted[9]] = []
            DRUG[splitted[9]].append(splitted[5])
        else:
            DRUG[splitted[9]].append(splitted[5])

# p = re.compile()

with open('test.txt', 'w') as note01:
    for dg in DRUG:
        therapy = ', '.join(sorted(set(DRUG[dg])))
        AAChange = dg.split('.')[1]
        position = re.findall(r'\d+', AAChange)
        position = ''.join(position)
        Ref = AAChange.split(position)[0]
        Alt = AAChange.split(position)[1]
        if 'delins' in Alt:
            Alt = Alt.replace('delins','')
        
        if len(list(Ref)) > 1:
            Ref = list(Ref)
            Ref = [CONVERT[aa] for aa in Ref]
            Ref = ''.join(Ref)
            result = Ref + str(position) + CONVERT[Alt]
            note01.write('ABL1' + '\t' + AAChange + '\t' + result + '\t' + therapy + '\n')
        elif len(list(Alt)) > 1:
            Alt = list(Alt)
            Alt = [CONVERT[aa] for aa in Alt]
            Alt = ''.join(Alt)
            result = CONVERT[Ref] + str(position) + 'delins' + Alt
            note01.write('ABL1' + '\t' + AAChange + '\t' + result + '\t' + therapy + '\n')
        else:
            if 'Z' in Alt:
                for aa in CONVERT[Alt].split(','):
                    result = CONVERT[Ref] + str(position) + CONVERT[aa]
                    AAChange2 = AAChange.replace('Z', aa)
                    note01.write('ABL1' + '\t' + AAChange2 + '\t' + result + '\t' + therapy + '\n')
            else:
                result = CONVERT[Ref] + str(position) + CONVERT[Alt]
                note01.write('ABL1' + '\t' + AAChange + '\t' + result + '\t' + therapy + '\n')