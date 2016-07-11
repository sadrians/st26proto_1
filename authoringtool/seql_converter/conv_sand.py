import re
import os

from converter import St25To26Converter 
 
import converter_util as cu 


# for el in cu.ELEMENT_NAME_ST26:
#     print el 
    
# # calculate number of chars per tag: 4 angle brackets plus one slash plus 2*length of tag name
TAG_LENGTH_ST26 = {}
for el in cu.ELEMENT_NAME_ST26:
    TAG_LENGTH_ST26[el] = 5 + 2*len(el)
     
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













# def multiple_replace(text, adict):
# #     https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
#     rx = re.compile('|'.join(map(re.escape, adict)))
#     def one_xlat(match):
#         return adict[match.group(0)]
#     return rx.sub(one_xlat, text)
# 
# s = 'Met Glu Thr Lys Ala Ile Ile'
# 
# 
# PRT_REGEX = "Ala|Arg|Asn|Asp|Cys|Glu|Gln|Gly|His|Ile|Leu|Lys|Met|Phe|Pro|Ser|Thr|Trp|Tyr|Val|Xaa|Asx|Glx|Xle|Pyl|Sec"
# aa = PRT_REGEX.split('|')
# # print aa 
# AMINO_ACIDS = {'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 
# 'Cys': 'C', 'Glu': 'E', 'Gln': 'Q', 'Gly': 'G', 
# 'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K', 
# 'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S', 
# 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V', 
# 'Xaa': 'X', 'Asx': 'B', 'Glx': 'Z', 'Xle': 'J', 
# 'Pyl': 'O', 'Sec': 'U'}
# 
# # print multiple_replace(s.replace(' ', ''), AMINO_ACIDS)

