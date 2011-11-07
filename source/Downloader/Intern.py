'''
Created on 05.11.2011

@author: DuncanMCLeod
'''

import Downloader
import urllib.request
import SQLs
import os

class Intern(Downloader):
    '''Downloadklasse die mithilfe von den Pythonklassen die Dateien herunterlaedt'''


    def download(self, id, castFileName, url, status):
        # Datei NEU oder beim letzten Versuch nen Fehler jehabt?
        if (status==SQLs.episodestatus["new"]) or (status==SQLs.episodestatus["error"]): 
            castFile = open(castFileName, 'wb')
            castFile.write(urllib.request.urlopen(url).read())
            castFile.close()
        # Datei Unvollstaendig?
        elif (status==SQLs.episodestatus["incomplete"]):
            sizeOfcastFile = os.path.getsize(castFileName)
            castFile = open(castFileName, 'ab')
            downloaddingens = urllib.request.urlopen(url)
            castFile.write(downloaddingens.read().seek(sizeOfcastFile))
            castFile.close()
