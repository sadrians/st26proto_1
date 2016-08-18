# -*- coding: utf-8 -*-
'''
Created on Jul 25, 2016

@author: ad
'''
import chardet
import codecs
import io
import os 
import converter_util as cu 

if __name__ == "__main__":
    tf = 'combined_lengths.csv'
    wf = 'encoding_test.txt'
    
    d = r'/Users/ad/pyton/projects/test'
    fp = os.path.join(d, 'Guidance_Document_SEQL-2.xml')
    fp_out = os.path.join(d, 'Guidance_Document_SEQL-2_clean.xml')
    
    with open(fp, 'r') as f, open(fp_out, 'w') as wr:
#         print cu.removeEmptyLinesFromString(f) 
        wr.write(cu.removeEmptyLinesFromString(f))
    
#     f63219 = 'st25parser/testData/WO2012-063219-001.zip.txt'
#     
#     with open(f63219, 'r') as f:
#         s = f.read()
#         print chardet.detect(s)
#     with open(f63219, 'r') as f:
#         s = f.read()
#         u = s.decode('windows-1252')
#         print type(u)
#         
#         un = u.encode('utf-8')
#         print chardet.detect(un)
        
#     s = '上海市第一人民医院'
#     
#     print 'length of s', len(s)
#     enc = chardet.detect(s)['encoding']
#     print 'encoding of s', enc 
#     u = s.decode(enc)
#     print 'length of u', len(u)
#     fp = 'sand.txt'
#     with open(fp, 'w') as wr:
#         wr.write(u.encode('utf-8'))
#         
#     print 'file size', os.path.getsize(fp)
#     
#     with open(fp, 'r') as f:
#         print 'length of string in file', len(f.read())

# s = 'hi猫'
# s = 'abc'
# print s
# print len(s)
# print type(s)
# print chardet.detect(s)
# 
# u = unicode(s, 'utf-8')
# print u 
# print u[2]
# print len(u)
# print type(u)
# 
# 
# # print chardet.detect(u)
# b = u.encode('utf-8')
# print b 
# print len(b)
# print type(b)
# print chardet.detect(b)

# with codecs.open(tf, 'r') as f:
#     s = f.read()
#     print chardet.detect(s)
#     
#     with codecs.open(wf, 'w', encoding='utf-8') as w:
#         w.write(unicode(s))
# 
# with codecs.open(wf, 'r') as f:
#     s = f.read()
#     print chardet.detect(s)

# with io.open(tf, 'rb') as f:
#     s = f.read()
#     print chardet.detect(s)
#     
#     with io.open(wf, 'w', encoding='utf8') as w:
#         w.write(unicode(s.encode('utf-8')))
# 
# with open(wf, 'r') as f:
#     s = f.read()
#     print chardet.detect(s)