'''
Created on 05.11.2011

@author: DuncanMCLeod
'''

import Downloader
import urllib.request

class Intern(Downloader):
    '''Downloadklasse die mithilfe von den Pythonklassen die Dateien herunterlaedt'''


    def download(self, id, castFileName, url, status):
        castFile = open(castFileName, 'wb')
        castFile.write(urllib.request.urlopen(url).read())
        castFile.close()
