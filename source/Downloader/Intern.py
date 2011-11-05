'''
Created on 05.11.2011

@author: DuncanMCLeod
'''

import urllib.request

class Intern(object):
    '''
    classdocs
    '''


    def __init__(self,params):
        '''
        Constructor
        '''


    def download(self, castFileName, url):
        castFile = open(castFileName, 'wb')
        castFile.write(urllib.request.urlopen(url).read())
        castFile.close()