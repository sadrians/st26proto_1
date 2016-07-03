'''
Created on Jul 2, 2016

@author: ad
'''
import re 

AMINO_ACIDS = {'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 
'Cys': 'C', 'Glu': 'E', 'Gln': 'Q', 'Gly': 'G', 
'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K', 
'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S', 
'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V', 
'Xaa': 'X', 'Asx': 'B', 'Glx': 'Z', 'Xle': 'J', 
'Pyl': 'O', 'Sec': 'U'}

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
                iPOfficeCode = 'XX'
                applicationNumberText = anApplicationNumber
            else:
                firstTwoChars = anApplicationNumber[:2]
                if re.match('\D\D', firstTwoChars):
                    iPOfficeCode = firstTwoChars.strip()
                    applicationNumberText = anApplicationNumber[2:].strip()
                else:
                    iPOfficeCode = 'XX'
                    applicationNumberText = anApplicationNumber
        else:
            iPOfficeCode = 'XX'
            applicationNumberText = anApplicationNumber
        
        
    return(iPOfficeCode, applicationNumberText)

def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text) 