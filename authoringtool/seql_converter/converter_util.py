'''
Created on Jul 2, 2016

@author: ad
'''
import re
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

def getSt26ElementNames():
    res = []
    with open(slsu.XML_DTD_PATH, 'r') as f:
        for l in f:
            if '<!ELEMENT ' in l:
    #             print l 
                elementName = ELEMENT_DTD_LINE_PATTERN.search(l).group('elementName')
    #             print elementName
    #             print '='*50
                res.append(elementName)
    return res 

ELEMENT_NAME_ST26 = getSt26ElementNames()

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
    applicationNumberText = '-'
    
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



    
