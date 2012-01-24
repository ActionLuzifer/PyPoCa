'''
Created on 05.11.2011

@author: DuncanMCLeod
'''

import Downloader.BasisDownloader
import urllib.request
import SQLs
import os
import sys

class Intern(Downloader.BasisDownloader.Downloader):
    '''Downloadklasse die mithilfe von den Pythonklassen die Dateien herunterlaedt'''
   
    def download(self, id, castFileName, url, status):
        fileOptions = ''
        #sizeOfcastFile = 0
        # Datei NEU oder beim letzten Versuch nen Fehler jehabt?
        if (status==SQLs.episodestatus["new"]) or (status==SQLs.episodestatus["error"]):
            fileOptions = 'wb' 
        # Datei Unvollstaendig?
        elif (status==SQLs.episodestatus["incomplete"]):
            fileOptions = 'ab'
            #try:
            #    sizeOfcastFile = os.path.getsize(castFileName)
            #except:
            #    exctype, value = sys.exc_info()[:2]
            #    print("ERROR"+exctype)
            #    print("   ->"+value)
            #    #sizeOfcastFile = 0
            #    fileOptions = 'wb'

        try:
            castFile = open(castFileName, fileOptions)
            downloaddingens = urllib.request.urlopen(url)
            #castFile.write(downloaddingens.read().seek(sizeOfcastFile))
            castFile.write(downloaddingens.read())
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR"+exctype)
            print("   ->"+value)
        finally:
            castFile.close()
