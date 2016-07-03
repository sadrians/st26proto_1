'''
Created on Jul 2, 2016

@author: ad
'''
import re 

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
