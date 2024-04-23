import xml.etree.ElementTree as ET

def process_sections(xml_file):
    header = ['NM', 'NMsequenceAccession', 'NMsequenceVersion', 'NMchange', 'Type', 'Symbol' ,'MANESelect', 'NPsequenceAccession', 'NPsequenceVersion', 'NPchange', 'AlleleID', 'RCV', 'Class', 'Synonym', 'Disease Info', 'Strand']
    context = ET.iterparse(xml_file, events=('start', 'end'))
    _, root = next(context)
    
    with open('Clinvar.annotation.txt', 'w') as note1:
        note1.write('\t'.join(header) + '\n')
        for event, elem in context:
            Total = {}
            if event == 'start' and elem.tag == 'ClassifiedRecord':
                HGVSList = elem.findall('./SimpleAllele/HGVSlist/HGVS')
                for hgvslist in HGVSList:
                    if hgvslist.attrib['Type'] == 'coding':
                        if hgvslist.find('NucleotideExpression') is not None: 
                            if hgvslist.find('NucleotideExpression').attrib['sequenceAccession'].startswith('NM'):
                                Type = hgvslist.find('MolecularConsequence')
                                if Type is not None:
                                    Type = hgvslist.find('MolecularConsequence').attrib['Type']
                                    NM_accession = hgvslist.find('NucleotideExpression').attrib
                                    Total[NM_accession.get('sequenceAccessionVersion')] = {}
                                    Total[NM_accession.get('sequenceAccessionVersion')]['NM'] = NM_accession.get('sequenceAccession') + '.' + NM_accession.get('sequenceVersion')
                                    if 'MANESelect' in NM_accession:
                                        Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'O'
                                    else:
                                        Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'X'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['NMchange'] = NM_accession.get('change')
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Type'] = Type

                                    Symbol = elem.find("SimpleAllele/GeneList/Gene")
                                    if Symbol is not None:
                                        Symbol = Symbol.get('Symbol')
                                    else:
                                        Symbol = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Symbol'] = Symbol

                                    if hgvslist.find("ProteinExpression") != None:
                                        ProteinExpression = hgvslist.find("ProteinExpression").attrib
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = ProteinExpression.get('sequenceAccession')
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = ProteinExpression.get('sequenceVersion')
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = ProteinExpression.get('change')
                                    else:
                                        sequenceAccession = '.'
                                        sequenceVersion = '.'
                                        change = '.'
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = sequenceAccession
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = sequenceVersion
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = change

                                    Allele_ID = elem.find("SimpleAllele")
                                    Allele_ID = Allele_ID.get("AlleleID")
                                    Total[NM_accession.get('sequenceAccessionVersion')]['AlleleID'] = Allele_ID

                                    RCV = elem.find("RCVList/RCVAccession")
                                    if RCV is not None:
                                        RCV_accession = RCV.attrib['Accession']
                                    else:
                                        RCV_accession = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['RCV'] = RCV_accession

                                    Fullname = elem.find("SimpleAllele/GeneList/Gene")
                                    if Fullname is not None:
                                        FullName = Fullname.get('FullName')
                                    else:
                                        FullName = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['FullName'] = FullName
                                    #--------------------------------------------------------------------------------------#
                                    Location = elem.find("SimpleAllele/GeneList/Gene/Location/CytogeneticLocation")
                                    if Location is not None:
                                        Location = Location.text
                                    else:
                                        Location = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Location'] = Location
                                    #--------------------------------------------------------------------------------------#
                                    OMIM = elem.find("SimpleAllele/GeneList/Gene/OMIM")
                                    if OMIM is not None:
                                        OMIM = OMIM.text
                                    else:
                                        OMIM = '.' 
                                    Total[NM_accession.get('sequenceAccessionVersion')]['OMIM'] = OMIM
                                    #--------------------------------------------------------------------------------------#
                                    Strand = elem.find("SimpleAllele/GeneList/Gene/Location/SequenceLocation[@Assembly='GRCh37']")
                                    if Strand is not None:
                                        Strand = Strand.get('Strand')
                                    else:
                                        Strand = '.' 
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Strand'] = Strand
                                    #--------------------------------------------------------------------------------------# 
                                    Class = elem.find("Classifications/GermlineClassification/Description")
                                    if Class is not None:
                                        Class = Class.text
                                    else:
                                        Class = '.' 

                                    Synonym =  elem.find("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Symbol/ElementValue")
                                    if Synonym is not None:
                                        Synonym = Synonym.text
                                    else:
                                        Synonym = '.' 

                                    Disease_elem =  elem.findall("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Name")
                                    DISESE_INFO = []
                                    for (num, di) in enumerate(Disease_elem):
                                        Contents = di.find("ElementValue")
                                        if Contents is not None:
                                            Contents = f'[{num+1}] {di.find("ElementValue").text}'
                                            DISESE_INFO.append(Contents)
                                        else:
                                            Contents = '.' 
                                            DISESE_INFO.append(Contents)
                                    DISESE_INFO = (', '.join(DISESE_INFO))

                                    Total[NM_accession.get('sequenceAccessionVersion')]['Class'] = Class
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Synonym'] = Synonym
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Disease Info'] = DISESE_INFO

                                else :
                                    Type = '.'
                                    NM_accession = hgvslist.find('NucleotideExpression').attrib
                                    Total[NM_accession.get('sequenceAccessionVersion')] = {}
                                    Total[NM_accession.get('sequenceAccessionVersion')]['NM'] = NM_accession.get('sequenceAccession') + '.' + NM_accession.get('sequenceVersion')
                                    if 'MANESelect' in NM_accession:
                                        Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'O'
                                    else:
                                        Total[NM_accession.get('sequenceAccessionVersion')]['MANESelect'] = 'X'                                    
                                    Total[NM_accession.get('sequenceAccessionVersion')]['NMchange'] = NM_accession.get('change')
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Type'] = Type

                                    Symbol = elem.find("SimpleAllele/GeneList/Gene")
                                    if Symbol is not None:
                                        Symbol = Symbol.get('Symbol')
                                    else:
                                        Symbol = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Symbol'] = Symbol

                                    if hgvslist.find("ProteinExpression") != None:
                                        ProteinExpression = hgvslist.find("ProteinExpression").attrib
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = ProteinExpression.get('sequenceAccession')
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = ProteinExpression.get('sequenceVersion')
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = ProteinExpression.get('change')
                                    else:
                                        sequenceAccession = '.'
                                        sequenceVersion = '.'
                                        change = '.'
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceAccession'] = sequenceAccession
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPsequenceVersion'] = sequenceVersion
                                        Total[NM_accession.get('sequenceAccessionVersion')]['NPchange'] = change

                                    Allele_ID = elem.find("SimpleAllele")
                                    Allele_ID = Allele_ID.get("AlleleID")
                                    Total[NM_accession.get('sequenceAccessionVersion')]['AlleleID'] = Allele_ID

                                    RCV = elem.find("RCVList/RCVAccession")
                                    if RCV is not None:
                                        RCV_accession = RCV.attrib['Accession']
                                    else:
                                        RCV_accession = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['RCV'] = RCV_accession

                                    Fullname = elem.find("SimpleAllele/GeneList/Gene")
                                    if Fullname is not None:
                                        FullName = Fullname.get('FullName')
                                    else:
                                        FullName = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['FullName'] = FullName
                                    #--------------------------------------------------------------------------------------#
                                    Location = elem.find("SimpleAllele/GeneList/Gene/Location/CytogeneticLocation")
                                    if Location is not None:
                                        Location = Location.text
                                    else:
                                        Location = '.'
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Location'] = Location
                                    #--------------------------------------------------------------------------------------#
                                    OMIM = elem.find("SimpleAllele/GeneList/Gene/OMIM")
                                    if OMIM is not None:
                                        OMIM = OMIM.text
                                    else:
                                        OMIM = '.' 
                                    Total[NM_accession.get('sequenceAccessionVersion')]['OMIM'] = OMIM
                                    #--------------------------------------------------------------------------------------#
                                    Strand = elem.find("SimpleAllele/GeneList/Gene/Location/SequenceLocation[@Assembly='GRCh37']")
                                    if Strand is not None:
                                        Strand = Strand.get('Strand')
                                    else:
                                        Strand = '.' 
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Strand'] = Strand
                                    #--------------------------------------------------------------------------------------# 
                                    Class = elem.find("Classifications/GermlineClassification/Description")
                                    if Class is not None:
                                        Class = Class.text
                                    else:
                                        Class = '.' 
                                    Synonym =  elem.find("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Symbol/ElementValue")
                                    if Synonym is not None:
                                        Synonym = Synonym.text
                                    else:
                                        Synonym = '.'

                                    Disease_elem =  elem.findall("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Name")
                                    DISESE_INFO = []
                                    for (num, di) in enumerate(Disease_elem):
                                        Contents = di.find("ElementValue")
                                        if Contents is not None:
                                            Contents = f'[{num+1}] {di.find("ElementValue")}'
                                            DISESE_INFO.append(Contents)
                                        else:
                                            Contents = '.' 
                                            DISESE_INFO.append(Contents)
                                    DISESE_INFO = (', '.join(DISESE_INFO))

                                    Total[NM_accession.get('sequenceAccessionVersion')]['Class'] = Class
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Synonym'] = Synonym
                                    Total[NM_accession.get('sequenceAccessionVersion')]['Disease Info'] = DISESE_INFO

                for key in Total.keys():
                    for vkey in Total[key].keys():
                        if Total[key][vkey] is None:
                            Total[key][vkey] = '.'

                # print(len(Total.values()))
                if len(Total.values()) >= 1 :
                    for key in Total.keys():
                        Value = Total[key].values()
                        Value = '\t'.join(Value) + '\n'
                        note1.write(Value)

if __name__ == "__main__":
    xml_file = "/media/src/Classification/ClinVarVCVRelease_00-latest_weekly.xml"
    process_sections(xml_file)