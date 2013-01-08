'''
Created on 05.11.2011

@author: DuncanMCLeod
'''

import source.Downloader.BasisDownloader as BasisDownloader
import urllib.request
import source.SQLs as SQLs
import sys

class Intern(BasisDownloader.Downloader):
    '''Downloadklasse die mithilfe von den Pythonklassen die Dateien herunterlaedt'''
   
    def download(self, id, castFileName, url, status):
        isError = False
        fileOptions = ''
        # Datei NEU oder beim letzten Versuch nen Fehler jehabt?
        if (status==SQLs.episodestatus["new"]) or (status==SQLs.episodestatus["error"]):
            fileOptions = 'wb' 
        # Datei Unvollstaendig?
        elif (status==SQLs.episodestatus["incomplete"]):
            fileOptions = 'ab'

        try:
            castFile = open(castFileName, fileOptions)
            downloaddingens = urllib.request.urlopen(url)
            castFile.write(downloaddingens.read())
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR"+repr(exctype))
            print("   ->"+repr(value))
            isError = True
        finally:
            castFile.close()
        return isError
