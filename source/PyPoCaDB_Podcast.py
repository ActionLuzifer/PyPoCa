'''
Created on 27.09.2011

@author: DuncanMCLeod
'''

import source.SQLs as SQLs
import sys
import source.Episode as Episode
import source.public_functions as public_functions

class PyPoCaDB_Podcast():
    
    def __init__(self, _DB):
        self.mDB = _DB


    def getPodcastInfosByCastID(self, castID):
        result = self.executeCommand(SQLs.sqlSELECTpodcasts, (castID,), True)
        return result[0]


    def getHighestEpisodeIDByCastID(self, castID):
        # TODO: was wenn numbersQuery leer ist?
        numbersQuery = self.executeCommand(SQLs.sqlSELECTcastsAndEpisodes, (castID,), True)
        for number in numbersQuery:
            return number[0]


    def setHighestEpisodeIDByCastID(self, castID, episodeID):
        self.executeCommand(SQLs.sqlUPDATEcastsAndEpisodes, (castID, episodeID), True)


    def episodes_INSERT(self, castID, episodeID, episodeURL, episodeName, episodeGUID):
        sql = SQLs.sqlINSERTepisodes
        return self.executeCommand(sql, (castID, episodeID, episodeURL, episodeName, episodeGUID, 1), True)


    def insertEpisodes(self, episodes, castID):
        ''' erwartet eine Liste von Episoden, die die Url und den Namen der Folge beinhalten, und die ID des Podcasts
        '''
        episodeID = self.getHighestEpisodeIDByCastID(castID)
        try:
            try:
                for episode in episodes:
                    if not self.episodes_INSERT(castID, episodeID+1, episode.episodeURL, public_functions.f_replaceBadSQLChars(episode.episodeName), episode.episodeGUID)==0:
                        episodeID = episodeID+1   # episodeID wird nur um eins erhoeht wenn die SQL-Abfrage keinen Fehler verursacht hat
                    else:
                        raise Exception()
            except:
                print("ERROR@PyPoCaDB_Podcast:insertEpisodes")
                exctype, value = sys.exc_info()[:2]
                print("ERROR: "+repr(exctype))
                print("       "+repr(value))
                raise exctype
                
        finally:
            self.setHighestEpisodeIDByCastID(castID, episodeID)
            self.writeChanges()


    def updateEpisodeURL(self, castID, episodeID, newURL):
        self.executeCommand(SQLs.sqlUPDATEepisodes_episodeURL, (newURL, castID, episodeID), True)


    def updateEpisodeName(self, castID, episodeID, newName):
        self.executeCommand(SQLs.sqlUPDATEepisodes_episodeNAME, (newName, castID, episodeID), True)


    def episodes_SELECTbyCast(self, castID):
        sql = SQLs.sqlSELECTepisodesByCast
        return self.executeCommand(sql, (castID, ), True)


    def executeCommand(self, command, args=None, hasArgs=False):
        return self.mDB._executeCommand(command, args, hasArgs)
    
    
    def getAllEpisodesByCastID(self, castID):
        episodesQuery = self.episodes_SELECTbyCast(castID)
        episodes = []
        for qepisode in episodesQuery:
            episode = Episode.Episode(qepisode[0], qepisode[1], qepisode[2], 
                                      qepisode[3], qepisode[4], qepisode[5])
            episodes.append(episode)
        return episodes


    def episodes_UPDATEstatus(self, castID, episodeID, status):
        sql = SQLs.sqlUPDATEepisodes_status
        return self.executeCommand(sql, (SQLs.episodestatus[status], castID, episodeID), True)

    
    def updateEpisodeStatus(self, episode, status):
        self.episodes_UPDATEstatus(episode.castID, episode.episodeID, status)


    def writeChanges(self):
        self.mDB.writeChanges()
