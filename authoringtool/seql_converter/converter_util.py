'''
Created on Jul 2, 2016

@author: ad
'''
import re
import os
import csv 
import chardet 
from django.conf import settings 

import sequencelistings.util as slsu 

AMINO_ACIDS = {'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 
'Cys': 'C', 'Glu': 'E', 'Gln': 'Q', 'Gly': 'G', 
'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K', 
'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S', 
'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V', 
'Xaa': 'X', 'Asx': 'B', 'Glx': 'Z', 'Xle': 'J', 
'Pyl': 'O', 'Sec': 'U'}

ST_25_ST_26_ELEMENT_MAP = {
    'ST26SequenceListing': 0,
    'ApplicantFileReference': 130,
    'ApplicationIdentification': 0,
    'EarliestPriorityApplicationIdentification': 0,
    'ApplicantName': 110,
    'ApplicantNameLatin': 0,
    'InventorName': 0,
    'InventorNameLatin': 0,
    'InventionTitle': 120,
    'SequenceTotalQuantity': 160,
    'SequenceData': 0,
    'IPOfficeCode': 140, # also 150
    'ApplicationNumberText': 140,  # also 150
    'FilingDate': 140, # also 151
    'INSDSeq': 0,
    'INSDSeq_length': 211,
    'INSDSeq_moltype': 212,
    'INSDSeq_division': 0,
    'INSDSeq_other': 0,
    'INSDSeq_feature': 220, #?
    'INSDSeq_sequence': 0,
    'INSDSeqid': 210,
    'INSDFeature': 220, #?
    'INSDFeature_key': 221,
    'INSDFeature_location': 222,
    'INSDFeature_quals': 0,
    'INSDQualifier': 0,
    'INSDQualifier_name': 0,
    'INSDQualifier_value': 223,

                           }

elementDtdLineRegex = r'<!ELEMENT (?P<elementName>\w+)'
ELEMENT_DTD_LINE_PATTERN = re.compile(elementDtdLineRegex)

DEFAULT_CODE = 'XX' # placeholder when IPOffice code or language code are missing
DEFAULT_DATE_STRING = '1900-01-01'
BLANK_PLACEHOLDER = '-'
CSV_HEADER = ['element_st25', 'seqIdNo', 
                         'element_st25_length', 
                         'value_length', 
                         'tag_st26_length', 
                         'element_st26_length', 
                         'element_st26', 
                         'comment']

FILE = 'file'
ELEMENT_ST25 = 'st25_tag' 
SEQ_ID_NO = 'seqIdNo'
ELEMENT_ST25_LENGTH = 'st25_raw'
VALUE_LENGTH = 'st25_val'
TAG_ST26_LENGTH = 'tag_st26_length' 
ELEMENT_ST26_LENGTH = 'element_st26_length' 
ELEMENT_ST26 = 'element_st26'
COMMENT = 'comment'

CDP_TXT = 'cdp_txt'
SIZE_TXT = 'size_txt_B'
CDP_XML = 'cdp_xml'
SIZE_XML = 'size_xml_B'
CDP_XML_CLEAN = 'cdp_xml_clean'
SIZE_XML_CLEAN = 'size_xml_clean_B'

SEQUENCES_TOT = 'q_tot'
SEQUENCES_NUC = 'q_nuc'
SEQUENCES_PRT = 'q_prt'
SEQUENCES_MIX = 'q_mix'

FEATURES_TOT = 'q_ftr'

RESIDUES_NUC = 'r_nuc'
RESIDUES_PRT = 'r_prt'

ENCODING_TXT = 'encoding_txt'
ENCODING_XML = 'encoding_xml'

CHARS_XML_CLEAN_VS_TXT = 'chars_xml_clean_vs_txt_ratio'
CHARS_XML_VS_TXT = 'chars_xml_vs_txt_ratio'

SIZE_XML_VS_TXT_RATIO = 'size_xml_vs_txt_ratio'
SIZE_XML_CLEAN_VS_TXT_RATIO = 'size_xml_clean_vs_txt_ratio'

STATS_HEADER = [FILE, SEQUENCES_TOT, SEQUENCES_NUC, SEQUENCES_PRT, SEQUENCES_MIX,
                FEATURES_TOT, 
                RESIDUES_NUC, RESIDUES_PRT,
                CDP_TXT, SIZE_TXT, 
                ENCODING_TXT,
                CDP_XML, SIZE_XML, SIZE_XML_VS_TXT_RATIO,
                CDP_XML_CLEAN, SIZE_XML_CLEAN, SIZE_XML_CLEAN_VS_TXT_RATIO, 
                ENCODING_XML
                ]

# STATS_HEADER = [FILE, SEQUENCES_TOT, SEQUENCES_NUC, SEQUENCES_PRT, SEQUENCES_MIX, 
#                 ELEMENT_ST25_LENGTH, VALUE_LENGTH, TAG_ST26_LENGTH, 
#                 ELEMENT_ST26_LENGTH, 
#                 CDP_TXT, SIZE_TXT, 
#                 ENCODING_TXT,
#                 CDP_XML, SIZE_XML, SIZE_XML_VS_TXT_RATIO,
#                 CDP_XML_CLEAN, SIZE_XML_CLEAN, SIZE_XML_CLEAN_VS_TXT_RATIO, 
#                 ENCODING_XML
#                 ]

# STATS_HEADER = [FILE, SEQUENCES_TOT, SEQUENCES_NUC, SEQUENCES_PRT, SEQUENCES_MIX, 
#                 ELEMENT_ST25_LENGTH, VALUE_LENGTH, TAG_ST26_LENGTH, 
#                 ELEMENT_ST26_LENGTH, CDP_TXT, SIZE_TXT, ENCODING_TXT,
#                 CDP_XML, SIZE_XML, CHARS_XML_VS_TXT,
#                 CDP_XML_CLEAN, SIZE_XML_CLEAN, CHARS_XML_CLEAN_VS_TXT, 
#                 ENCODING_XML
#                 ]

# CSV_HEADER_DICT = {'ELEMENT_ST25': 'element_st25', 
#                 'SEQ_ID_NO': 'seqIdNo', 
#                 'ELEMENT_ST25_LENGTH': 'element_st25_length', 
#                 'VALUE_LENGTH': 'value_length', 
#                 'TAG_ST26_LENGTH': 'tag_st26_length', 
#                 'ELEMENT_ST26_LENGTH': 'element_st26_length', 
#                 'ELEMENT_ST26': 'element_st26', 
#                 'COMMENT': 'comment'}

# def safeLength(aStr):
#     if aStr is not None:
#         return len(aStr)
#     else:
#         return 0

def safeLength(aStr):
    if aStr not in [None, '-']:
        return len(aStr)
    else:
        return 0


# def setSt26ElementLength():
#     res = {}
#     fp = os.path.join(settings.BASE_DIR, 'seql_converter', 'tags_st26.txt')
#     with open(fp) as f:
#         for line in f:
#             res[line.strip()] = 5 + 2*len(line.strip())
#     return res 

def setSt26ElementLength():
    res = {}
    fp = os.path.join(settings.BASE_DIR, 'seql_converter', 'tags_st26.txt')
    with open(fp) as f:
        for line in f:
            cleanLine = line.strip()
            if cleanLine[0].islower(): #it's an attribute
                res[cleanLine] = len(cleanLine) + 2*len('"') + len('=') + len(' ')
            else: #it's an element
                res[cleanLine] =  2*(len(cleanLine) + len('<') + len('>')) + len('/')
    return res

TAG_LENGTH_ST26 = setSt26ElementLength()

OTHER_ELEMENTS_ST26 = {
    'xmlHeader': '<?xml version="1.0" encoding="UTF-8"?>', 
    'doctypeDeclaration': '<!DOCTYPE ST26SequenceListing PUBLIC "-//WIPO//DTD Sequence Listing 1.0//EN" "resources/ST26SequenceListing_V1_0.dtd">',
    'styleSheetReference': '<?xml-stylesheet type="text/xsl" href="resources/st26.xsl"?>',  
    }
 
GENERAL_INFORMATION_SIZE = 900

SEQUENCE_MARKUP_SIZE = sum([TAG_LENGTH_ST26['SequenceData'],
                            TAG_LENGTH_ST26['sequenceIDNumber'],
                            TAG_LENGTH_ST26['INSDSeq'],
                            TAG_LENGTH_ST26['INSDSeq_length'],
                            TAG_LENGTH_ST26['INSDSeq_moltype'],
                            TAG_LENGTH_ST26['INSDSeq_division'],
                            TAG_LENGTH_ST26['INSDSeq_sequence']]) #210

SEQUENCE_SIZE = sum([SEQUENCE_MARKUP_SIZE, 
                            len('DNA'), 
                            len("PAT")]) # ignore value of sequenceIdNumber, length

QUALIFIER_MARKUP_SIZE = sum([TAG_LENGTH_ST26['INSDQualifier'],
                    TAG_LENGTH_ST26['INSDQualifier_name'],
                    TAG_LENGTH_ST26['INSDQualifier_value']])

FEATURE_MARKUP_SIZE = sum([TAG_LENGTH_ST26['INSDFeature'], 
                    TAG_LENGTH_ST26['INSDFeature_key'],
                    TAG_LENGTH_ST26['INSDFeature_location'],
                    TAG_LENGTH_ST26['INSDFeature_quals']]
                    )

# longest feature key is misc_difference 15 chars
FEATURE_VALUE_SIZE = sum([len('misc_difference'), 
                          len('1..1000'), 
                          len('note'),
                          130]) 

FEATURE_SOURCE_SIZE = sum([FEATURE_MARKUP_SIZE,
                           2*QUALIFIER_MARKUP_SIZE,
                           len('source'),
                           len('1..1000'), 
                           len('organism'),
                           20, #some value for organism value length
                           len('mol_type'),
                           len('genomic DNA')
                           ]) #399 + 34

FEATURE_SIZE = FEATURE_MARKUP_SIZE + QUALIFIER_MARKUP_SIZE + FEATURE_VALUE_SIZE #300
    
# ======================================================


def multiple_replace(text, adict):
#     https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

def oneLetterCode(res):
    return multiple_replace(res, AMINO_ACIDS)

def applicationNumberAsTuple(anApplicationNumber):
    
    iPOfficeCode = '--'
    applicationNumberText = ''
    
    if anApplicationNumber:
        if len(anApplicationNumber) > 1:
            if anApplicationNumber == 'Not yet assigned':
                iPOfficeCode = DEFAULT_CODE
                applicationNumberText = anApplicationNumber
            else:
                firstTwoChars = anApplicationNumber[:2]
                if re.match('\D\D', firstTwoChars):
                    iPOfficeCode = firstTwoChars.strip()
                    applicationNumberText = anApplicationNumber[2:].strip()
                else:
                    iPOfficeCode = DEFAULT_CODE
                    applicationNumberText = anApplicationNumber
        else:
            iPOfficeCode = DEFAULT_CODE
            applicationNumberText = anApplicationNumber
        
        
    return(iPOfficeCode, applicationNumberText)

def removeSpaces(aString):#is it used?
    regex = r'\s+<'
    p = re.compile(regex)
    return p.sub('<', aString) 
            
            
def compareGeneralInformation(aList, outDirPath, xmlOutDirPath):
    outf = os.path.join(outDirPath, 'genInfo_comparison.csv')
    with open(outf, 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        wr.writerow(['file', 'chars_gi_st25', 
                     'chars_gi_st25_clean',
                     'chars_gi_st25_value',
                      'chars_gi_st26', 
                      'chars_tot_st26_clean'])
        for fp in aList:
            bn = os.path.basename(fp)
            fileName = bn[:-4]
            print fileName
            xmlFileName = '%s_ST26_clean.xml' % fileName 
            print xmlFileName
            xmlFileNamePath = os.path.join(xmlOutDirPath, xmlFileName)
            
            with open(fp, 'r') as f25, open(xmlFileNamePath, 'r') as f26:
                genInfo25 = f25.read().split('<210>')[0]
#                 print genInfo25
#                 remove end of line chars
                cleanLines = [l.strip() for l in genInfo25.splitlines()]
                
#                 genInfo25_clean = re.sub(r'\s', '', genInfo25)
                genInfo25_clean = ''.join(cleanLines)
#                 print 'st25 clean', genInfo25_clean
                genInfo25_value = re.sub(r'<\d\d\d>\s', '', genInfo25_clean)
#                 print genInfo25_value
                string_st26 = f26.read()
                genInfo26 = string_st26.split('<SequenceData sequenceIDNumber="1">')[0]
#                 print genInfo26
                wr.writerow([bn, len(genInfo25), 
                             len(genInfo25_clean), 
                             len(genInfo25_value), 
                             len(genInfo26), 
                             len(string_st26)])

def getNumberOfCharsFromFile(aFilePath):
    with open(aFilePath, 'r') as f:
        return len(f.read())    

def cleanAndWriteXmlFile(anXmlFilePath):
    outFile = anXmlFilePath.replace('.xml', '_clean.xml')
    with open(anXmlFilePath, 'r') as f, open(outFile, 'w') as wr:

        clean = re.sub(r'\s+<', '<', f.read()).replace(os.linesep, '')
        clean = re.sub(r'>\s+', '>', clean)
        charEncoding = chardet.detect(clean)['encoding']
        u = clean.decode(charEncoding)
        wr.write(u.encode('utf-8'))
#         print 'Generated clean xml file', outFile 
    return outFile 

def getMarkupLength(aString):
    reg = '<.*?>'
    p = re.compile(reg)
    
    li = p.findall(aString)
    
    return sum([len(el) for el in li])

def removeEmptyLinesFromString(aString):
    return ''.join(line for line in aString if not line.isspace())
    
    
    