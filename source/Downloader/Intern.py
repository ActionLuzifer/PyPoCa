'''
Created on 05.11.2011

@author: DuncanMCLeod
'''

import Downloader
import urllib.request

class Intern(Downloader):
    '''
    classdocs
    '''


    def download(self, castFileName, url):
        castFile = open(castFileName, 'wb')
        castFile.write(urllib.request.urlopen(url).read())
        castFile.close()