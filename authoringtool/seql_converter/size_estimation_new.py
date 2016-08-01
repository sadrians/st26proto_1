'''
Created on Jul 12, 2016

@author: ad
'''
import re 
import os 
import csv
import io 
import pprint
import chardet
import converter_util as cu 
from converter import St25To26Converter 
import st25parser.seqlutils as su 

import st25parser.seqlparser_new 



class ElementSizeCalculator(object):
    def __init__(self, aFilePath):
        self.filePath = aFilePath
        self.seql = st25parser.seqlparser_new.SequenceListing(self.filePath)
        self.generalInformationRows = []
        self.sequenceRows = []
        if self.seql.isSeql:
            self.setRow_xmlRoot()
            self.setRow_doctypeDeclaration()
            self.setRow_styleSheetReference()
            self.setRow_header()
            self.setRow_dtdVersion()
            self.setRow_fileName()
            self.setRow_softwareName()
            self.setRow_softwareVersion()
            self.setRow_productionDate()
            self.setRow_110()
            self.setRow_InventorName()
            self.setRow_120()
            self.setRow_130()
            self.setRow_ApplicationIdentification()
            self.setRow_IPOfficeCode140()
            self.setRow_140()
            self.setRow_141()
    
            if self.seql.priorities:
                self.setRow_EarliestPriorityApplicationIdentification()
                self.setRow_IPOfficeCode150()
                self.setRow_150()
                self.setRow_151()
#                 self.setRow_prio()
            self.setRow_160()
            self.setRow_170()
            self.sequenceRows = self.setSequenceRows()
     
    def _getSt25St26Lengths(self,
                        element_st25_tag, 
                        seqIdNo,
                        element_st25, 
                        value_st25, 
                        element_st26, comment):
        
        return [element_st25_tag, 
                seqIdNo,
                cu.safeLength(element_st25), 
                cu.safeLength(value_st25),
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26],
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26] + 
                                    cu.safeLength(value_st25),
                element_st26, 
                comment
                ]    

    def setRow_xmlRoot(self):
        self.generalInformationRows.append([0, 0, 0, 0,
                len(cu.OTHER_ELEMENTS_ST26['xmlHeader']),
                len(cu.OTHER_ELEMENTS_ST26['xmlHeader']),
                'xmlHeader', 
                'ST.26 specific element'])
        
    def setRow_doctypeDeclaration(self):
        self.generalInformationRows.append([0, 0, 0, 0,
                len(cu.OTHER_ELEMENTS_ST26['doctypeDeclaration']),
                len(cu.OTHER_ELEMENTS_ST26['doctypeDeclaration']),
                'doctypeDeclaration', 
                'ST.26 specific element'])

    def setRow_styleSheetReference(self):
        self.generalInformationRows.append([0, 0, 0, 0,
                len(cu.OTHER_ELEMENTS_ST26['styleSheetReference']),
                len(cu.OTHER_ELEMENTS_ST26['styleSheetReference']),
                'styleSheetReference', 
                'ST.26 specific element'])

    def setRow_header(self):
        self.generalInformationRows.append([0, 0, 
                cu.safeLength(self.seql.seqlHeader_raw),
                cu.safeLength(self.seql.seqlHeader),
                cu.TAG_LENGTH_ST26['ST26SequenceListing'],
                cu.TAG_LENGTH_ST26['ST26SequenceListing'],
                'ST26SequenceListing', 
                'ST.25 seqlHeader discarded'])
    
    def setRow_dtdVersion(self):
        dtdVersionValue = 'd.d'
        self.generalInformationRows.append([0, 0, 
                0,
                len(dtdVersionValue),
                cu.TAG_LENGTH_ST26['dtdVersion'],
                len(dtdVersionValue) + cu.TAG_LENGTH_ST26['dtdVersion'],
                'dtdVersion', 
                'ST.26 specific element. Assumed format: d.d (for ex.: 1.3)'])
    
    def setRow_fileName(self):
#         file name without extension
        fileName = os.path.basename(self.filePath)[:-4]
        
        self.generalInformationRows.append([0, 0, 
                0,
                len(fileName),
                cu.TAG_LENGTH_ST26['fileName'],
                len(fileName) + cu.TAG_LENGTH_ST26['fileName'],
                'fileName', 
                'ST.25 file name used with extension xml'])
    
    def setRow_softwareName(self):
        lenSoftwareNameValue = 10
        self.generalInformationRows.append([0, 0, 
                0,
                lenSoftwareNameValue,
                cu.TAG_LENGTH_ST26['softwareName'],
                lenSoftwareNameValue + cu.TAG_LENGTH_ST26['softwareName'],
                'softwareName', 
                'ST.26 specific element. Assumed it has 10 chars'])
    
    def setRow_softwareVersion(self):
        softwareVersion = 'd.d'
        self.generalInformationRows.append([0, 0, 
                0,
                len(softwareVersion),
                cu.TAG_LENGTH_ST26['softwareVersion'],
                len(softwareVersion) + cu.TAG_LENGTH_ST26['softwareVersion'],
                'softwareVersion', 
                'ST.26 specific element. Assumed format: d.d (for ex.: 1.3)'])
        
    def setRow_productionDate(self):
        productionDate = 'YYYY-MM-DD'
        self.generalInformationRows.append([0, 0, 
                0,
                len(productionDate),
                cu.TAG_LENGTH_ST26['productionDate'],
                len(productionDate) + cu.TAG_LENGTH_ST26['productionDate'],
                'productionDate', 
                'ST.26 specific element. Assumed format: YYYY-MM-DD (for ex.: 2013-10-20. Date format is still to be implemented in the prototype tool)'])
        
    def setRow_110(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(110, 0,
            self.seql.applicant_raw,
            self.seql.applicant[0],
            'ApplicantName', cu.BLANK_PLACEHOLDER))
        
        self.generalInformationRows.append(self._getSt25St26Lengths(110, 0,
            '-', cu.DEFAULT_CODE,
            'languageCode', 'ST.26 specific languageCode attribute for ApplicantName'))

    def setRow_InventorName(self):
        r = [0, 0, 
                0,
                0,
                cu.TAG_LENGTH_ST26['InventorName'],
                1 + cu.TAG_LENGTH_ST26['InventorName'],
                'InventorName', 
                cu.BLANK_PLACEHOLDER]
        self.generalInformationRows.append(r)
        
        self.generalInformationRows.append(self._getSt25St26Lengths(0, 0,
            cu.BLANK_PLACEHOLDER, cu.DEFAULT_CODE,
            'languageCode', 'ST.26 specific languageCode attribute for InventorName'))
        
    def setRow_120(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(120, 0,
            self.seql.title_raw,
            self.seql.title,
            'InventionTitle', cu.BLANK_PLACEHOLDER))
        
        self.generalInformationRows.append(self._getSt25St26Lengths(120, 0,
            '-', cu.DEFAULT_CODE,
            'languageCode', 'ST.26 specific languageCode attribute for InventionTitle'))
        
    def setRow_130(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(130, 0,
            self.seql.reference_raw,
            self.seql.reference,
            'ApplicantFileReference', cu.BLANK_PLACEHOLDER))
#     TODO: include in calculation IPOffice element!
 
    def setRow_ApplicationIdentification(self):
        r = [0, 0, 
                0,
                0,
                cu.TAG_LENGTH_ST26['ApplicationIdentification'],
                cu.TAG_LENGTH_ST26['ApplicationIdentification'],
                'ApplicationIdentification', 
                cu.BLANK_PLACEHOLDER]
        
        self.generalInformationRows.append(r)
         
    def setRow_IPOfficeCode140(self):
        r = [0, 0, 
                0,
                0,
                cu.TAG_LENGTH_ST26['IPOfficeCode'],
                2 + cu.TAG_LENGTH_ST26['IPOfficeCode'],
                'IPOfficeCode', 
                'Corresponding to 140. XX placeholder for the purpose of this study']
        
        self.generalInformationRows.append(r)
        
    def setRow_140(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(140, 0, 
            self.seql.applicationNumber_raw,
            self.seql.applicationNumber,
            'ApplicationNumberText', cu.BLANK_PLACEHOLDER))
     
    def setRow_141(self):
        #         set filingDate
        fd = self.seql.filingDate
        if fd != cu.BLANK_PLACEHOLDER:
            filingDateAsString = fd 
        else:
            filingDateAsString = cu.DEFAULT_DATE_STRING
        
        self.generalInformationRows.append(self._getSt25St26Lengths(141, 0, 
            self.seql.filingDate_raw,
            filingDateAsString,
            'FilingDate', cu.BLANK_PLACEHOLDER))
    
    def setRow_EarliestPriorityApplicationIdentification(self):
        r = [0, 0, 
                0,
                0,
                cu.TAG_LENGTH_ST26['EarliestPriorityApplicationIdentification'],
                cu.TAG_LENGTH_ST26['EarliestPriorityApplicationIdentification'],
                'EarliestPriorityApplicationIdentification', 
                cu.BLANK_PLACEHOLDER]
        
        self.generalInformationRows.append(r)
         
    def setRow_IPOfficeCode150(self):
        r = [0, 0, 
                0,
                0,
                cu.TAG_LENGTH_ST26['IPOfficeCode'],
                2 + cu.TAG_LENGTH_ST26['IPOfficeCode'],
                'IPOfficeCode', 
                'Corresponding to 150. XX placeholder for the purpose of this study']
        
        self.generalInformationRows.append(r)
    
    def setRow_150(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(150, 0, 
            self.seql.priorities_raw,
            self.seql.priorities[0][0],
            'ApplicationNumberText', 'only first ST.25 priority retained, if any'))
        
    def setRow_151(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(151, 0, 
            cu.BLANK_PLACEHOLDER,
            self.seql.priorities[0][1],
            'FilingDate', 'chars of raw prio counted for already in 150'))
            
    def setRow_160(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(160, 0, 
            self.seql.quantity_raw,
            self.seql.quantity,
            'SequenceTotalQuantity', cu.BLANK_PLACEHOLDER))
    
    def setRow_170(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(170, 0, 
            self.seql.software_raw,
            self.seql.software,
            cu.BLANK_PLACEHOLDER, 'information discarded in ST.26'))

    
    def setSequenceRows(self):
        res = []
        
        sequences = self.seql.sequences
                
        for seq in sequences:
            
# ====================== 210 ======================
            currentRow_SequenceData = self._getSt25St26Lengths(0, seq.seqIdNo, 
                            '-', '-', 'SequenceData', 
                            'ST.26 specific element')

            res.append(currentRow_SequenceData)
            
            currentRow210 = self._getSt25St26Lengths(210, seq.seqIdNo, 
                            seq.seqIdNo_raw, seq.seqIdNo, 'sequenceIDNumber', '-')

            res.append(currentRow210)
            
            currentRow_INSDSeq = self._getSt25St26Lengths(0, seq.seqIdNo, 
                            '-', '-', 'INSDSeq', 'ST.26 specific element')

            res.append(currentRow_INSDSeq)

# ====================== 211 ======================            
            currentRow211 = self._getSt25St26Lengths(211, seq.seqIdNo, 
                            seq.length_raw, seq.length, 'INSDSeq_length', cu.BLANK_PLACEHOLDER)
            res.append(currentRow211)

# ====================== 212 ======================            
            moltypeValue = 'AA' if seq.molType == 'PRT' else seq.molType 

            currentRow212 = [212, seq.seqIdNo, cu.safeLength(seq.molType_raw), 
                            cu.safeLength(seq.molType), 
                            cu.TAG_LENGTH_ST26['INSDSeq_moltype'], 
                            cu.safeLength(moltypeValue) + cu.TAG_LENGTH_ST26['INSDSeq_moltype'],
                            'INSDSeq_moltype', 
                            'PRT replaced by AA for proteins' if moltypeValue == 'AA' else cu.BLANK_PLACEHOLDER]
            
            res.append(currentRow212)

# ====================== INSDSeq_division ======================            
            INSDSeq_division_val = 'PAT'
            currentRow_INSDSeq_division = self._getSt25St26Lengths(0, seq.seqIdNo, 
                            '-', INSDSeq_division_val, 'INSDSeq_division', 
                            'ST.26 specific element')
            res.append(currentRow_INSDSeq_division)

# ====================== INSDSeq_other-seqids ======================
# optional element, therefore not included in calculations

# ====================== INSDSeq_feature-table ======================            
            currentRow_INSDSeq_feature_table = self._getSt25St26Lengths(0, 
                            seq.seqIdNo, 
                            '-', '-', 'INSDSeq_feature-table', 
                            'ST.26 specific element')
            res.append(currentRow_INSDSeq_feature_table)

# ====================== 213 ======================                        
#             create ST.26 feature source
            currentRow_INSDFeature = [0, seq.seqIdNo, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature'], 
                            cu.TAG_LENGTH_ST26['INSDFeature'],
                            'INSDFeature', 
                            'ST.26 mandatory feature source']
            res.append(currentRow_INSDFeature)
            
            currentRow_INSDFeature_key = [0, seq.seqIdNo, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature_key'], 
                            len('source') + cu.TAG_LENGTH_ST26['INSDFeature_key'],
                            'INSDFeature_key', 
                            'ST.26 mandatory feature source']
            
            res.append(currentRow_INSDFeature_key)
            
            sourceLocation = '1..%s' % seq.length
            currentRow_INSDFeature_location = [0, seq.seqIdNo, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature_location'], 
                            len(sourceLocation) + cu.TAG_LENGTH_ST26['INSDFeature_location'],
                            'INSDFeature_location', 
                            'ST.26 mandatory feature source']
            
            res.append(currentRow_INSDFeature_location)
            
            def append_INSDFeature_quals(msg):
                res.append([0, seq.seqIdNo, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature_quals'], 
                            cu.TAG_LENGTH_ST26['INSDFeature_quals'],
                            'INSDFeature_quals', 
                            msg])
            
#             add first the parent element INSDFeature_quals
            append_INSDFeature_quals('ST.26 mandatory feature source')
            
            def createQualifier(name, msg):
                currentRow_INSDQualifier = [0, seq.seqIdNo, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDQualifier'], 
                            cu.TAG_LENGTH_ST26['INSDQualifier'],
                            'INSDQualifier', 
                            msg]
            
                res.append(currentRow_INSDQualifier)
                
                currentRow_INSDQualifier_name = [0, seq.seqIdNo, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDQualifier_name'], 
                            len(name) + cu.TAG_LENGTH_ST26['INSDQualifier_name'],
                            'INSDQualifier_name', 
                            msg]
            
                res.append(currentRow_INSDQualifier_name)
            
            def createQualifierValue(tag_st25, element_st25, value_st25, msg):
                
                currentRow_INSDQualifier_value = [tag_st25, 
                    seq.seqIdNo, cu.safeLength(element_st25), 
                    cu.safeLength(value_st25), 
                    cu.TAG_LENGTH_ST26['INSDQualifier_value'], 
                    cu.safeLength(value_st25) + cu.TAG_LENGTH_ST26['INSDQualifier_value'],
                    'INSDQualifier_value', 
                    msg]
            
                res.append(currentRow_INSDQualifier_value)
            
#             qualifier organism
            createQualifier('organism', 'ST.26 mandatory qualifier organism')
            createQualifierValue(213, seq.organism_raw, 
                            seq.organism, 
                            'ST.26 mandatory qualifier organism')

#             qualifier mol_type
            mol_typeValue = 'protein' if seq.molType == 'PRT' else 'genomic DNA'
            createQualifier('mol_type', 'ST.26 mandatory qualifier mol_type') 
#             createQualifierValue(0, 0, mol_typeValue, 'ST.26 mandatory qualifier mol_type')
            res.append([0, seq.seqIdNo, 0, 0,  
                    cu.TAG_LENGTH_ST26['INSDQualifier_value'], 
                    cu.safeLength(mol_typeValue) + cu.TAG_LENGTH_ST26['INSDQualifier_value'],
                    'INSDQualifier_value', 
                    'ST.26 mandatory qualifier mol_type'])
            
#             end create ST.26 feature source

# ====================== other features ======================        
            parsedFeatures = seq.features
            for feat in seq.features:
                currentFeatureIndex = seq.features.index(feat)
                parsedFeature = parsedFeatures[currentFeatureIndex]
                isSimpleFeature = False
                if parsedFeature.key == cu.BLANK_PLACEHOLDER and parsedFeature.location == cu.BLANK_PLACEHOLDER:
                    isSimpleFeature = True 
                if not isSimpleFeature:
                    # ====================== 220 ======================                
                    currentRow220 = self._getSt25St26Lengths(220, seq.seqIdNo, 
                                feat.featureHeader_raw, parsedFeature.featureHeader, 
                                'INSDFeature', cu.BLANK_PLACEHOLDER)
                    res.append(currentRow220)
    
                    # ====================== 221 ======================                
                    currentRow221 = self._getSt25St26Lengths(221, seq.seqIdNo, 
                                feat.key_raw, parsedFeature.key, 
                                'INSDFeature_key', cu.BLANK_PLACEHOLDER)
                    res.append(currentRow221)
    
                    # ====================== add row for mixed mode translation qualifier ======================                               
                    if parsedFeature.key == 'CDS':
                        createQualifier('translation', 'ST.26 specific element translation')
                        translationRow = [400, seq.seqIdNo, 
                                0, 
                                cu.safeLength(parsedFeature.translation),
                                cu.TAG_LENGTH_ST26['INSDQualifier_value'],
                                (cu.TAG_LENGTH_ST26['INSDQualifier_value'] + 
                                len(cu.oneLetterCode(parsedFeature.translation))),
                                'INSDQualifier_value', '3-to-1 letter code']
                        
                        res.append(translationRow)
    
                    # ====================== 222 ======================                
                    currentRow222 = self._getSt25St26Lengths(222, seq.seqIdNo, 
                                feat.location_raw, parsedFeature.location, 
                                'INSDFeature_location', cu.BLANK_PLACEHOLDER)
                    res.append(currentRow222)
                
# ====================== 223 ======================                
                if parsedFeature.description != cu.BLANK_PLACEHOLDER: #do not add row if 223 missing!
                    append_INSDFeature_quals('ST.26 mandatory element')
                    createQualifier('note', cu.BLANK_PLACEHOLDER)
                    createQualifierValue(223, feat.description_raw, 
                                        parsedFeature.description, 
                                        cu.BLANK_PLACEHOLDER)
                                   
# ====================== 400 ======================        
            if seq.molType == 'PRT':
                parsedResidues = seq.residues_prt
                currentRow400 = [400, seq.seqIdNo, 
                            cu.safeLength(seq.residues_raw), 
                            cu.safeLength(parsedResidues),
                            cu.TAG_LENGTH_ST26['INSDSeq_sequence'],
                            (cu.TAG_LENGTH_ST26['INSDSeq_sequence'] + 
                            len(cu.oneLetterCode(parsedResidues))),
                            'INSDSeq_sequence', '3-to-1 letter code']
                
            else:
                parsedResidues = seq.residues_nuc
                currentRow400 = self._getSt25St26Lengths(400, seq.seqIdNo, 
                                seq.residues_raw, parsedResidues, 
                                'INSDSeq_sequence', cu.BLANK_PLACEHOLDER)
            res.append(currentRow400)
        
        return res 
        
    def writeSizes(self, outDirPath):
        bname = os.path.basename(self.filePath)
        inFileName = bname.split('.')[0]
        
        outFilePath = os.path.join(outDirPath, '%s_element_size.csv' % inFileName)
        
        with open(outFilePath, 'wb') as csvfile:
            wr = csv.writer(csvfile, delimiter=',')
            wr.writerow(cu.CSV_HEADER)
            
            for genInfoRow in self.generalInformationRows:
                wr.writerow(genInfoRow)
            for seqRow in self.sequenceRows:
                wr.writerow(seqRow)
#         print 'Generated file', outFilePath
        
        return outFilePath

class FileSizeComparator(object):
    def __init__(self, inFilePath, outDirPath, xmlOutDirPath):
        self.inFilePath = inFilePath 
        self.outDirPath = outDirPath
        self.xmlOutDirPath = xmlOutDirPath
        
        self.esc = ElementSizeCalculator(self.inFilePath)
        if self.esc.seql.isSeql:
            self.csvFilePath = self.esc.writeSizes(self.outDirPath)
                        
            sc = St25To26Converter(self.inFilePath)
            self.xmlFilePath = sc.generateXmlFile(self.xmlOutDirPath)
    
            self.cleanXmlFilePath = self.cleanAndWriteXmlFile() 
            
            self.totals = {}
                        
            self.setTotals() 
        else:
            print 'FileSizeComparator: not able to process', inFilePath
    
    def cleanAndWriteXmlFile(self):
        outFile = self.xmlFilePath.replace('.xml', '_clean.xml')
        with open(self.xmlFilePath, 'r') as f, open(outFile, 'w') as wr:

            clean = re.sub(r'\s+<', '<', f.read()).replace(os.linesep, '')
            clean = re.sub(r'>\s+', '>', clean)
            charEncoding = chardet.detect(clean)['encoding']
            u = clean.decode(charEncoding)
            wr.write(u.encode('utf-8'))
#         print 'Generated clean xml file', outFile 
        return outFile 
           
    def setTotals(self):
        rows = self.esc.generalInformationRows + self.esc.sequenceRows 
        
        self.totals[cu.FILE] = os.path.basename(self.inFilePath)
        self.totals[cu.QUANTITY] = self.esc.seql.quantity
        self.totals[cu.SEQUENCES_NUC] = self.esc.seql.quantity_nuc
        self.totals[cu.SEQUENCES_PRT] = self.esc.seql.quantity_prt
        self.totals[cu.MIXED_MODE] = self.esc.seql.quantity_mix  
        self.totals[cu.ELEMENT_ST25_LENGTH] = sum([r[2] for r in rows])
        self.totals[cu.VALUE_LENGTH] = sum([r[3] for r in rows])
        self.totals[cu.TAG_ST26_LENGTH] = sum([r[4] for r in rows])
        self.totals[cu.ELEMENT_ST26_LENGTH] = sum([r[5] for r in rows])
        
        with open(self.inFilePath, 'r') as inf:
            s_txt = inf.read()
            self.totals[cu.CHARS_TXT_FILE] = len(s_txt)
            self.totals[cu.ENCODING_TXT] = chardet.detect(s_txt)['encoding']
        self.totals[cu.FILE_SIZE_TXT] = os.path.getsize(self.inFilePath)

        with open(self.xmlFilePath, 'r') as f:
            s_xml = f.read()
            self.totals[cu.CHARS_XML_FILE] = len(s_xml)
            
        self.totals[cu.FILE_SIZE_XML] = os.path.getsize(self.xmlFilePath) 

        with open(self.cleanXmlFilePath, 'r') as f:
            s_xml = f.read()
            self.totals[cu.CHARS_XML_CLEAN_FILE] = len(s_xml)
            self.totals[cu.ENCODING_XML] = chardet.detect(s_xml)['encoding']
        self.totals[cu.FILE_SIZE_XML_CLEAN] = os.path.getsize(self.cleanXmlFilePath) 
        
        ratio = self.totals[cu.CHARS_XML_FILE]/float(self.totals[cu.CHARS_TXT_FILE])
        
        self.totals[cu.CHARS_XML_VS_TXT] = '%0.2f' % ratio
        
        ratio_clean = self.totals[cu.CHARS_XML_CLEAN_FILE]/float(self.totals[cu.CHARS_TXT_FILE])
        
        self.totals[cu.CHARS_XML_CLEAN_VS_TXT] = '%0.2f' % ratio_clean
        
        print self.inFilePath
        print 'encoding:', self.esc.seql.charEncoding

    def compareElementsInCsvAndXmlFiles(self):
        
        def countSt26ElementsFromCsvFile():
            res = {}
            rows = self.esc.generalInformationRows + self.esc.sequenceRows 
            
            for el in cu.TAG_LENGTH_ST26.keys():
                currentRows = [r for r in rows if r[6] == el]
                res[el] = len(currentRows)
            return res 
        
        def countSt26ElementsFromXmlFile():
            res = {}
            with open(self.cleanXmlFilePath, 'r') as f:
                xmlString = f.read()
                for el in cu.TAG_LENGTH_ST26.keys():
                    if el[0].islower():
                        currentElement = el
                    else:
                        currentElement = '</%s>' % el 
                    res[el] = xmlString.count(currentElement)
            return res
        
        countCsv = countSt26ElementsFromCsvFile()
        countXml = countSt26ElementsFromXmlFile()
        
        for el in cu.TAG_LENGTH_ST26:
            c = countCsv[el]
            x = countXml[el]
            if c != x:
                print el
                print '%d in csv' %c, '%d in xml' %x 
             
#     helper just to make sure that csv and xml contain (mostly) the same elements
    
#     def compareElementsInCsvAndXmlFiles(self):
#         
#         def countSt26ElementsFromCsvFile(inFilePath):
#             res = {}
#             esc = ElementSizeCalculator(inFilePath)
#             rows = esc.generalInformationRows + esc.sequenceRows 
#             
#             for el in cu.TAG_LENGTH_ST26.keys():
#                 currentRows = [r for r in rows if r[6] == el]
#                 res[el] = len(currentRows)
#             return res 
#         
#         def countSt26ElementsFromXmlFile(inFilePath):
#             res = {}
#             with open(inFilePath, 'r') as f:
#                 xmlString = f.read()
#                 for el in cu.TAG_LENGTH_ST26.keys():
#                     if el[0].islower():
#                         currentElement = el
#                     else:
#                         currentElement = '</%s>' % el 
#                     res[el] = xmlString.count(currentElement)
#             return res
#         
#         countCsv = countSt26ElementsFromCsvFile(self.csvFilePath)
# #         countXml = countSt26ElementsFromXmlFile(self.xmlFilePath)
#         
# #         for el in cu.TAG_LENGTH_ST26:
# #             c = countCsv[el]
# #             x = countXml[el]
# #             if c != x:
# #                 print el
# #                 print '%d in csv' %c, '%d in xml' %x 

#         def listTotals(self):
#             su.printHeader(self.inFilePath)
#             rows = self.esc.generalInformationRows + self.esc.sequenceRows 
#             
#             for i in range(2,6):
#                 print cu.CSV_HEADER[i], sum([r[i] for r in rows]) 
#             with open(self.inFilePath, 'r') as inf:
#                 print 'chars in txt file:', len(inf.read())
#             print 'ST.25 txt file size:', os.path.getsize(self.inFilePath)
#             
#             with open(self.cleanXmlFilePath, 'r') as f:
#                 s = f.read()
#                 print 'chars in xml clean file:', len(s)
#             print 'ST.26 xml file size:', os.path.getsize(self.cleanXmlFilePath) 