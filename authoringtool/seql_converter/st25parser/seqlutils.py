import re
# import datetime
import os
import logging
import logging.handlers
# import numpy as np

currentDirectory = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIRECTORY = os.path.abspath(os.path.join(currentDirectory, os.pardir))

####################
# logging setup
####################

logFile = os.path.join(PROJECT_DIRECTORY, 'log/slc_logger.log')

logging.basicConfig(filename=logFile,
                format='%(asctime)s - %(name)s - %(levelname)s\n\t%(message)s',
                level=logging.WARNING
                )

logger = logging.getLogger('seqlutils')
handler = logging.handlers.RotatingFileHandler(logFile, maxBytes=1000000)
logger.addHandler(handler)
# logger.info('seqlutils module loaded')

# logFile = os.path.join(PROJECT_DIRECTORY, 'log/statslogger.log')
#
# logging.basicConfig(filename=logFile,
#                     format='%(asctime)s %(message)s',
#                     level=logging.DEBUG)

seqlElementRegex = r'<\d\d\d>\s*(?P<elementValue>[^<]*)'
seqlElementPattern = re.compile(seqlElementRegex, re.DOTALL)

# ================================================
# regex
# ================================================
RANGE_LOCATION_REGEX = r'\(?(?P<startPos>\d+)\)?\.\.\.?\(?(?P<endPos>\d+)\)?'
RANGE_LOCATION_PATTERN = re.compile(RANGE_LOCATION_REGEX)

# ================================================
# constants
# ================================================
STOP_CODONS_DNA = ['tag', 'taa', 'tga']
STOP_CODONS_RNA = ['uag', 'uaa', 'uga']

DEFAULT_STRING = '-'
# ================================================
# functions
# ================================================

def inOneLine(aString):
    if aString:
        return " ".join(aString.split())
    else:
        return aString

def getElementValue(seqlElement):
    """
    Returns the value of a sequence listing data element.
    The pattern of seqlElement is <\d\d\d>\s*(?P<elementValue>[^<]*).
    """
    result = '-'
    m = seqlElementPattern.match(seqlElement)
    if m:
        g = m.group('elementValue')
        result = g.strip()
    return result


def printHeader(msg):
    print '=' * 70
    print msg
    print '=' * 70

def customTimeit(func, number, *args, **kwargs):
    import timeit

    def wrapper(func, *args, **kwargs):
        def wrapped():
            return func(*args, **kwargs)

        return wrapped

    g = wrapper(func, *args, **kwargs)

    print timeit.timeit(g, number=number)

def generateChunks(f, pa):
    """
    Read the text file f and yield a dictionary every time the pattern pa is
    encountered. The dictionary contains the lines read so far (key 'chunk') and
    the line number where the chunk started (key 'lineNumber'). Raises IOError
    if f does not exist.
    """
    # logger.info('Generator invoked with pattern %s for file: %s' % (pa, f))
    with open(f, 'r') as fi:
        reslist = []
        lineNumber = 1
        previousLineNumber = 1
        for line in fi:
            if pa in line:
                yield {'chunk': ''.join(reslist),
                       'lineNumber': previousLineNumber}
                reslist = []
                previousLineNumber = lineNumber
            reslist.append(line)
            lineNumber += 1
        yield {'chunk': ''.join(reslist), 'lineNumber': previousLineNumber}

def generateChunksFromString(inStr, pa):
    """
    Read lines from inStr and yield a dictionary every time the pattern pa is
    encountered. The dictionary contains the lines read so far (key 'chunk') and
    the line number where the chunk started (key 'lineNumber'). Raises IOError
    if f does not exist.
    """
    # logger.info('Generator invoked with pattern %s for file: %s' % (pa, f))
    reslist = []
    lineNumber = 1
    previousLineNumber = 1
    for line in inStr.splitlines(1):
        if pa in line:
            yield {'chunk': ''.join(reslist),
                   'lineNumber': previousLineNumber}
            reslist = []
            previousLineNumber = lineNumber
        reslist.append(line)
        lineNumber += 1
    yield {'chunk': ''.join(reslist), 'lineNumber': previousLineNumber}

def getRangeFromLocation(aLocation):
    res = (0,0)

    m = RANGE_LOCATION_PATTERN.match(aLocation)
    if m:
        startPos = m.group('startPos')
        endPos = m.group('endPos')
        res = (int(startPos), int(endPos))
    else:
        print 'The input location %s does not have the pattern %s' %(aLocation, RANGE_LOCATION_REGEX)

    return res

def safeStrip(s):
    if s is not None:
        return s.strip()
    else:
        return DEFAULT_STRING
    
def parsePriorities(aString):
    result = []
    reg = r'<150>\s+(?P<priorityNumber>[^<]+)<151>\s+(?P<priorityDate>[^<]+)'
    p = re.compile(reg, re.MULTILINE)
    if aString:
        for m in p.finditer(aString):
            result.append((safeStrip(m.group('priorityNumber')), 
                            safeStrip(m.group('priorityDate'))))         
    return result

# def findCdsNotDivByThree(aList, outfp):
#     with open(outfp, 'w') as wr:
#         for fp in aList:
#             print fp
#             seql = SequenceListing(fp)
#             for seq in seql.sequences:
#                 for f in seq.features:
#                     if f.key == 'CDS':
#                         locationRange = su.getRangeFromLocation(f.location) 
#                         if (locationRange[1] - locationRange[0] + 1)%3 != 0:
#                             wr.write('%s\n' % fp)
#                             wr.write('seq %s\n' % seq.seqIdNo)
#                             wr.write('loc %s\n' % f.location)
#                             
# def getStopCodon(aString, aList):
#     res = {}
#     codons = [aString[i:i+3] for i in xrange(0, len(aString), 3)]
#     for c in aList:
#         cou = 0
#         for cod in codons:
#             if c == cod:
#                 cou += 1
#         if cou > 0:
#             res[c] = (cou, aString.rfind(c))
#
#     return res

# def generateChunks(inStr, pa):
#     """
#     Read the text file f and yield a dictionary every time the pattern pa is
#     encountered. The dictionary contains the lines read so far (key 'chunk') and
#     the line number where the chunk started (key 'lineNumber'). Raises IOError
#     if f does not exist.
#     """
#     # logger.info('Generator invoked with pattern %s for file: %s' % (pa, f))
#     reslist = []
#     lineNumber = 1
#     previousLineNumber = 1
#     for line in inStr:
#         if pa in line:
#             yield {'chunk': ''.join(reslist),
#                    'lineNumber': previousLineNumber}
#             reslist = []
#             previousLineNumber = lineNumber
#         reslist.append(line)
#         lineNumber += 1
#     yield {'chunk': ''.join(reslist), 'lineNumber': previousLineNumber}

# test
# emailSand()


# # configuration
# config = ConfigParser.ConfigParser()
# configFile = os.path.join(PROJECT_DIRECTORY, 'config/config.ini')
# config.read(configFile)
#
# ASAP_INPUT_DIRECTORY = os.path.join(PROJECT_DIRECTORY, config.get('Directory', 'asapInputDirectory'))
# ASAP_DIRECTORY = os.path.join(PROJECT_DIRECTORY, config.get('Directory', 'asapDirectory'))
# # VERIF_DIRECTORY = os.path.join(PROJECT_DIRECTORY, config.get('Directory', 'verifDirectory'))
# # GDS_DIRECTORY = os.path.join(PROJECT_DIRECTORY, config.get('Directory', 'gdsDirectory'))
#
# # reports
# # TITLE_REPORT_DIRECTORY = os.path.join(PROJECT_DIRECTORY, config.get('Directory', 'titleReportDirectory'))
# # CONTENTS_REPORT_DIRECTORY = os.path.join(PROJECT_DIRECTORY, config.get('Directory', 'contentsReportDirectory'))
# # UPDATE_DIRECTORY = os.path.join(PROJECT_DIRECTORY, config.get('Directory', 'updateDirectory'))
#
# # verification reports files
# # GDS_REPORT_FILE = os.path.join(PROJECT_DIRECTORY, config.get('File', 'gdsReportFile'))
# # VERIFICATION_REPORT_FILE = os.path.join(PROJECT_DIRECTORY, config.get('File', 'verificationReportFile'))

