import re
import os
from django.conf import settings

from converter import St25To26Converter 
 
import converter_util as cu 

f5 = os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 'testData', 'file5.txt') 

def convertFile(inFile, outDir):
    sc = St25To26Converter(inFile)
    sc.generateXmlFile(outDir)
    print 'Converted to xml file', inFile

# convertFile(f5, '.')

# f5conv = 'file5_converted.xml'

# with open(f5conv, 'r') as f:
#     print f.read().replace(os.linesep, '')


# for el in cu.ELEMENT_NAME_ST26:
#     print el 
    
# # calculate number of chars per tag: 4 angle brackets plus one slash plus 2*length of tag name
# TAG_LENGTH_ST26 = {}
# for el in cu.ELEMENT_NAME_ST26:
#     TAG_LENGTH_ST26[el] = 5 + 2*len(el)
#      
# for k,v in TAG_LENGTH_ST26.iteritems():
#     print k,v 

# for el in cu.ELEMENT_NAME_ST26:
#     print '\'<>\': \'%s\',' % el 

# for el in cu.ELEMENT_NAME_ST26:
#     print '\'%s\': ,' % el 

# d_in = r'/Users/ad/pyton/test/converter_in'
# d_out = r'/Users/ad/pyton/test/converter_out'
# 
# l = [os.path.join(d_in, a) for a in os.listdir(d_in) if '.DS' not in a]
# 
# for fp in l:
#     print 'Processing file %s ...' %fp
#     sc = St25To26Converter(fp)
#     sc.generateXmlFile(d_out)
# print 'Done'
