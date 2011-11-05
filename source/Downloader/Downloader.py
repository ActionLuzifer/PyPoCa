'''
Created on 05.11.2011

@author: DuncanMCLeod
'''

import urllib.request

class Intern:
    '''
    classdocs
    '''


    def __init__(self, podcastObj, anzahlThreads):
        '''
        Constructor
        '''


    def download(self, castFileName, url):
        castFile = open(castFileName, 'wb')
        castFile.write(urllib.request.urlopen(url).read())
        castFile.close()