import sys
import re
import html.entities


def f_replaceBadCharsByRegEx(badstring):
    matches = re.findall("&#\d+;", badstring)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            name = hit[2:-1]
            try:
                entnum = int(name)
                badstring = badstring.replace(hit, chr(entnum))
            except ValueError:
                pass
            
    matches = re.findall("&#[xX][0-9a-fA-F]+;", badstring)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            hhex = hit[3:-1]
            try:
                entnum = int(hhex, 16)
                badstring = badstring.replace(hit, chr(entnum))
            except ValueError:
                pass

    matches = re.findall("&\w+;", badstring)
    hits = set(matches)
    for hit in hits:
        name = hit[1:-1]
        if name in html.entities.name2codepoint:
            badstring = badstring.replace(hit, chr(html.entities.name2codepoint[name]))
    
    return badstring

def f_replaceBadCharsFiles(mf_executeStr):
    mf_executeStr = mf_executeStr.replace("/", "-")
    mf_executeStr = f_replaceBadCharsPath(mf_executeStr)
    return mf_executeStr
    
def f_replaceBadCharsPath(mf_executeStr):
    mf_executeStr = mf_executeStr.replace(" ", "_")
    mf_executeStr = mf_executeStr.replace('"', "'")
    mf_executeStr = mf_executeStr.replace('“', "'")
    mf_executeStr = mf_executeStr.replace('”', "'")
    mf_executeStr = mf_executeStr.replace('&#8211;', "-")  #     Unicode Character 'EN DASH' (U+2013) - http://www.fileformat.info/info/unicode/char/2013/index.htm
    mf_executeStr = mf_executeStr.replace('&#8212;', "-")  #     Unicode Character 'EM DASH' (U+2014) - http://www.fileformat.info/info/unicode/char/2014/index.htm
    mf_executeStr = mf_executeStr.replace('&quot;', "'")
    
    mf_executeStr = f_replaceBadCharsByRegEx(mf_executeStr)
    
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        mf_executeStr = mf_executeStr.replace("?", "_")
        mf_executeStr = mf_executeStr.replace(":", "-")
    return mf_executeStr


def f_replaceBadSQLChars(mf_executeStr):
    mf_executeStr = mf_executeStr.replace("'", "\'")
    mf_executeStr = mf_executeStr.replace("&amp;", "&")
    
    return mf_executeStr


def getFindRegEx(searchstring, regexstring, groupname):
    REprogramm = re.compile(regexstring)
    foundObject = REprogramm.search(searchstring)
    return foundObject.group(groupname)
