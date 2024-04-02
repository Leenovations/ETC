from lxml import etree

tree = etree.parse('/media/src/Classification/test2.xml')
root = tree.getroot()
#--------------------------------------------------------------------------------------#
Info = root.findall("VariationArchive/ClassifiedRecord")
for info in Info:
    Allele_ID = info.find("SimpleAllele")
    Allele_ID = Allele_ID.get("AlleleID")
    print("AlleleID:", Allele_ID)
    #--------------------------------------------------------------------------------------#
    Gene = info.find("SimpleAllele/GeneList/Gene")
    gene = Gene.get('Symbol')
    print(gene)
    #--------------------------------------------------------------------------------------#
    Fullname = info.find("SimpleAllele/GeneList/Gene")
    FullName = Fullname.get('FullName')
    print(FullName)
    #--------------------------------------------------------------------------------------#
    Location = info.find("SimpleAllele/GeneList/Gene/Location/CytogeneticLocation")
    Location = Location.text
    print("Location:", Location)
    #--------------------------------------------------------------------------------------#
    Strand = info.find("SimpleAllele/GeneList/Gene/Location/SequenceLocation[@Assembly='GRCh37']")
    Strand = Strand.get('Strand')
    print("Strand:", Strand)
    #--------------------------------------------------------------------------------------#
    OMIM = info.find("SimpleAllele/GeneList/Gene/OMIM")
    OMIM = OMIM.text
    print("OMIM:", OMIM)
    #--------------------------------------------------------------------------------------#
    HGVSlist = info.findall("SimpleAllele/HGVSlist/HGVS/NucleotideExpression")
    for hgvslist in HGVSlist:
        if hgvslist.attrib['sequenceAccession'].startswith('NM'):
            NM_accession = hgvslist.attrib
            print(NM_accession.get('sequenceAccession'))
            print(NM_accession.get('sequenceVersion'))
            MolecularConsequence = hgvslist.find("../MolecularConsequence").attrib
            print(MolecularConsequence.get('Type'))
            if hgvslist.find("../ProteinExpression") != None:
                ProteinExpression = hgvslist.find("../ProteinExpression").attrib
                print(ProteinExpression.get('sequenceAccession'))
                print(ProteinExpression.get('sequenceVersion'))
                print(ProteinExpression.get('change'))
            else:
                sequenceAccession = None
                sequenceVersion = None
                change = None
                print(sequenceAccession)
                print(sequenceVersion)
                print(change)
    #--------------------------------------------------------------------------------------#
    RCV = info.find("RCVList/RCVAccession")
    RCV_accession = RCV.get('Accession')
    print("RCV_accession :", RCV_accession)
    #--------------------------------------------------------------------------------------#
    Class = info.find("Classifications/GermlineClassification/Description").text
    Synonym =  info.find("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Symbol/ElementValue").text
    Disease_info =  info.findall("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Name")

    DISESE_INFO = []
    for (num, di) in enumerate(Disease_info):
        Contents = f'[{num}] {di.find("ElementValue").text}'
        DISESE_INFO.append(Contents)
    DISESE_INFO = (', '.join(DISESE_INFO))
    
    print(Class)
    print(Synonym)
    print(DISESE_INFO)
    print('==============================================================================')
    #--------------------------------------------------------------------------------------#