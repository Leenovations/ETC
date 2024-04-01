from lxml import etree

tree = etree.parse('/media/src/Classification/test2.xml')
root = tree.getroot()
#--------------------------------------------------------------------------------------#
Info = root.findall("VariationArchive/ClassifiedRecord")
for info in Info:
    # Allele_ID = info.find("SimpleAllele")
    # Allele_ID = Allele_ID.get("AlleleID")
    # print("AlleleID:", Allele_ID)
    # #--------------------------------------------------------------------------------------#
    # Gene = info.find("SimpleAllele/GeneList/Gene")
    # gene = Gene.get('Symbol')
    # print(gene)
    # #--------------------------------------------------------------------------------------#
    # Fullname = info.find("SimpleAllele/GeneList/Gene")
    # FullName = Fullname.get('FullName')
    # print(FullName)
    # #--------------------------------------------------------------------------------------#
    # Location = info.find("SimpleAllele/GeneList/Gene/Location/CytogeneticLocation")
    # Location = Location.text
    # print("Location:", Location)
    # #--------------------------------------------------------------------------------------#
    # Location = info.find("SimpleAllele/GeneList/Gene/Location/SequenceLocation[@Assembly='GRCh37']")
    # print(Location)
    # print(Location.attrib)
    # Location = Location.get('Strand')
    # print("Location:", Location)
    # #--------------------------------------------------------------------------------------#
    # OMIM = info.find("SimpleAllele/GeneList/Gene/OMIM")
    # OMIM = OMIM.text
    # print("OMIM:", OMIM)
    # #--------------------------------------------------------------------------------------#
    HGVSlist = info.findall("SimpleAllele/HGVSlist/HGVS/NucleotideExpression")
    for hgvslist in HGVSlist:
        print(hgvslist.attrib)
    # for hgvslist in HGVSlist:
    #     if 'MANESelect' in hgvslist.attrib:
    #         print(hgvslist.attrib)
    # #--------------------------------------------------------------------------------------#
    HGVSlist = info.findall("SimpleAllele/HGVSlist/HGVS/")
    for hgvslist in HGVSlist:
        print(hgvslist.attrib)
        # if 'MANESelect' in hgvslist.attrib:
        #     print(hgvslist.attrib)
    # #--------------------------------------------------------------------------------------#
    # RCV = info.find("RCVList/RCVAccession")
    # RCV_accession = RCV.get('Accession')
    # print("RCV_accession :", RCV_accession)
    # #--------------------------------------------------------------------------------------#
    # Class = info.find("Classifications/GermlineClassification/Description").text
    # Synonym =  info.find("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Symbol/ElementValue").text
    # Disease_info =  info.findall("Classifications/GermlineClassification/ConditionList/TraitSet/Trait/Name")

    # DISESE_INFO = []
    # for (num, di) in enumerate(Disease_info):
    #     Contents = f'[{num}] {di.find("ElementValue").text}'
    #     DISESE_INFO.append(Contents)
    # DISESE_INFO = (', '.join(DISESE_INFO))
    
    # print(Class)
    # print(Synonym)
    # print(DISESE_INFO)
    # #--------------------------------------------------------------------------------------#