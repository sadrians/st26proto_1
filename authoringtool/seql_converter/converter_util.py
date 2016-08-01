'''
Created on Jul 2, 2016

@author: ad
'''
import re
import os
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
CHARS_TXT_FILE = 'chars_txt'
FILE_SIZE_TXT = 'size_txt_B'
FILE_SIZE_XML = 'size_xml_B'
CHARS_XML_FILE = 'chars_xml'
FILE_SIZE_XML_CLEAN = 'size_xml_clean_B'
CHARS_XML_CLEAN_FILE = 'chars_xml_clean'
QUANTITY = 'q_tot'
SEQUENCES_NUC = 'q_nuc'
SEQUENCES_PRT = 'q_prt'
MIXED_MODE = 'q_mix'
ENCODING_TXT = 'encoding_txt'
ENCODING_XML = 'encoding_xml'
CHARS_XML_CLEAN_VS_TXT = 'chars_xml_clean_vs_txt_ratio'
CHARS_XML_VS_TXT = 'chars_xml_vs_txt_ratio'

STATS_HEADER = [FILE, QUANTITY, SEQUENCES_NUC, SEQUENCES_PRT, MIXED_MODE, 
                ELEMENT_ST25_LENGTH, VALUE_LENGTH, TAG_ST26_LENGTH, 
                ELEMENT_ST26_LENGTH, CHARS_TXT_FILE, FILE_SIZE_TXT, ENCODING_TXT,
                CHARS_XML_FILE, FILE_SIZE_XML, CHARS_XML_VS_TXT,
                CHARS_XML_CLEAN_FILE, FILE_SIZE_XML_CLEAN, CHARS_XML_CLEAN_VS_TXT, 
                ENCODING_XML
                ]

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
            
            

    
