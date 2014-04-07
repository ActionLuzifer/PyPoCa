'''
Created on 12.03.2012

@author: ActionLuzifer
'''

import sys

class Episode:
    ''' beinhaltet die Daten einer Episode
    '''

    stdout_encoding = sys.stdout.encoding or sys.getfilesystemencoding()

    def __init__(self, castID, episodeID, episodeURL, episodeName, episodeGUID, episodeStatus, pubDate):
        self.castID        = castID
        self.episodeID     = episodeID
        self.episodeURL    = episodeURL
        self.episodeName   = episodeName
        self.episodeGUID   = episodeGUID
        self.episodeStatus = episodeStatus
        self.pubDate       = pubDate


    def getName(self):
        return self.episodeName


    def printName(self):
        try:
            eID = "{:0>4}".format(self.episodeID)
            print("----->", eID, " | ", self.episodeName.encode(self.stdout_encoding, 'ignore').decode('utf-8','ignore')) 
        except:
            print("Problem bei der Darstellung von einer Episode")
