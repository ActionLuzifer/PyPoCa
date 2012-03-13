'''
Created on 12.03.2012

@author: ActionLuzifer
'''


class Episode:
    ''' beinhaltet die Daten einer Episode
    '''
    def __init__(self, castID, episodeID, episodeURL, episodeName, episodeGUID, episodeStatus):
        self.castID        = castID
        self.episodeID     = episodeID
        self.episodeURL    = episodeURL
        self.episodeName   = episodeName
        self.episodeGUID   = episodeGUID
        self.episodeStatus = episodeStatus