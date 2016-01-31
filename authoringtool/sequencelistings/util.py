'''
Created on Apr 17, 2015

@author: ad
'''
import os, re

# from lxml import etree

currentDirectory = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIRECTORY = os.path.abspath(os.path.join(currentDirectory, os.pardir))

MOLTYPE_CHOICES = [('DNA', 'DNA'), ('RNA', 'RNA'), ('AA', 'AA')]

MOL_TYPE_QUALIFIER_VALUES = {'DNA': 'genomic DNA', 'RNA': 'genomic RNA', 'AA': 'protein'}

QUALIFIER_CHOICE = {'attenuator': [('allele', 'allele'),
                                    ('gene', 'gene'),
                                    ('gene_synonym', 'gene_synonym'),
                                    ('map', 'map'),
                                    ('note', 'note'),
                                    ('operon', 'operon'),
                                    ('phenotype', 'phenotype')],
                    'C_region': [('allele', 'allele'),
                                    ('gene', 'gene'),
                                    ('gene_synonym', 'gene_synonym'),
                                    ('map', 'map'),
                                    ('note', 'note'),
                                    ('product', 'product'),
                                    ('pseudo', 'pseudo'),
                                    ('pseudogene', 'pseudogene'),
                                    ('standard_name', 'standard_name')],
                    'CAAT_signal': [('allele', 'allele'),
                                    ('gene', 'gene'),
                                    ('gene_synonym', 'gene_synonym'),
                                    ('map', 'map'),
                                    ('note', 'note')],
                    }

def generate_list(inputFilePath):
    lis = []
    with open(inputFilePath, 'r') as f:
        for line in f:
            lis.append(line.strip())
    
    return lis 

fkdna = list(generate_list(os.path.join(PROJECT_DIRECTORY, 'sequencelistings', 'static', 'res', 'featureKey_dna.txt')))
fkprt = list(generate_list(os.path.join(PROJECT_DIRECTORY, 'sequencelistings', 'static', 'res', 'featureKey_prt.txt')))

FEATURE_KEYS_DNA = [(a, a) for a in fkdna] 
FEATURE_KEYS_PRT  = [(a, a) for a in fkprt] 

def rangeFromString(s):
#     s = 
    result = None # so no match
    rex = r'ra\((?P<startVal>\d+),(?P<stopVal>\d+),(?P<stepVal>\d+)\)'
    p = re.compile(rex)
    
    m = p.match(s)
    if m:
#         print 'match'
        try:
            startVal = int(m.group('startVal'))
            stopVal = int(m.group('stopVal'))
            stepVal = int(m.group('stepVal'))
            
#             print 'startVal', startVal
#             print 'stopVal', stopVal
#             print 'stepVal', stepVal
            
            result = range(startVal, stopVal, stepVal)
        except ValueError as ve:
            print '%s could not be converted to integer.' %s
            print ve
            
    return result

# def validateDocumentWithSchema(afile, aschema):
#     result = False
#     
#     with open(aschema, 'r') as fs:
#         try:
#             doc = etree.parse(fs)
#     
#             try:
#                 schema = etree.XMLSchema(doc)
#                 with open(afile, 'r') as ff:
#                     try:
#                         doc = etree.parse(ff)
#                         try:
#                             schema.assertValid(doc)
#                             result = True
#                         except etree.DocumentInvalid as e:
#                             print e
#                     except etree.XMLSyntaxError as e:
#                         print e 
#                 
#                     
#             except etree.XMLSchemaParseError as e:
#                 print e
#         except etree.XMLSyntaxError as e:
#             print e
#     return result
# 
# def validateDocumentWithDtd(afile, adtd):
#     result = False
#     with open(adtd, 'r') as d:
#         dtd = etree.DTD(d)
#         with open(afile, 'r') as f:
#             try:
#                 fi = etree.XML(f.read())
#                 if dtd.validate(fi):
#                     result = True
#     #                 print 'OK: File %s is valid against DTD %s.' %(afile, adtd)
#                 else:
#                     print(dtd.error_log.filter_from_errors()[0])
#             except etree.XMLSyntaxError as e:
#                         print e 
#     return result

# def validateDocumentWithDtd(afile, adtd):
#     with open(adtd, 'r') as d:
#         dtd = etree.DTD(d)
#         with open(afile, 'r') as f:
#             fi = etree.XML(f.read())
#             if dtd.validate(fi):
#                 print 'OK: File %s is valid against DTD %s.' %(afile, adtd)
#             else:
#                 print(dtd.error_log.filter_from_errors()[0])



# FEATURE_KEYS_DNA = [('fkd%d' % fkdna.index(a), a) for a in fkdna] 
# FEATURE_KEYS_PRT  = [('fkp%d' % fkprt.index(a), a) for a in fkprt] 

# FEATURE_KEYS_DNA_TUP = [('fkd%d' % FEATURE_KEYS_DNA.index(a), a) for a in FEATURE_KEYS_DNA]

# for e in FEATURE_KEYS_DNA_TUP:
#     print e


# for e in FEATURE_KEYS_DNA:
#     print e




# myf = 'xml_test.xml'
# mys = 'xml_test.xsd'

# def validateDocumentWithSchema(afile, aschema):
#     with open(aschema, 'r') as fs:
#         doc = etree.parse(fs)
# 
#         print "Validating schema %s... " % aschema
#         try:
#             schema = etree.XMLSchema(doc)
#         except etree.XMLSchemaParseError as e:
#             print e
#             exit(1)
#     
#         print "Schema OK"
#     
#         with open(afile, 'r') as ff:
#             doc = etree.parse(ff)
#     
#             print "Validating document %s..." % afile
#             try:
#                 schema.assertValid(doc)
#             except etree.DocumentInvalid as e:
#                 print e
#                 exit(1)
#         
#             print "Document OK" 
# 
# QUALIFIER_CHOICE = {'attenuator': ['allele', 
#                                     'gene', 
#                                     'gene_synonym', 
#                                     'map', 
#                                     'note', 
#                                     'operon',
#                                     'phenotype'],
#                     'C_region': ['allele', 
#                                     'gene', 
#                                     'gene_synonym', 
#                                     'map', 
#                                     'note', 
#                                     'product',
#                                     'pseudo',
#                                     'pseudogene',
#                                     'standard_name'],
#                     'CAAT_signal': ['allele', 
#                                     'gene', 
#                                     'gene_synonym', 
#                                     'map', 
#                                     'note'],
#                     }
# def validateDocumentWithSchema1(afile, aschema):
#     result = False
#     with open(aschema, 'r') as fs:
#         doc = etree.parse(fs)
# 
#         print "Validating schema %s... " % aschema
#         try:
#             schema = etree.XMLSchema(doc)
#             with open(afile, 'r') as ff:
#                 doc1 = etree.parse(ff)
#         
#                 print "Validating document %s..." % afile
#                 result = schema.validate(doc1)
#         except etree.XMLSchemaParseError as e:
#             print e
#             exit(1)
#     
#         print "Document OK"
#     return result

# def validateStringWithSchema(astring, aschema):
#     result = False
#     with open(aschema, 'r') as fs:
#         doc = etree.parse(fs)
# 
#         print "Validating schema %s... " % aschema
#         try:
#             schema = etree.XMLSchema(doc)
#             doc1 = etree.parse(astring)
#             result = schema.validate(doc1)
#         except etree.XMLSchemaParseError as e:
#             print e
#             exit(1)
#     
#         print "Document OK"
#     return result
