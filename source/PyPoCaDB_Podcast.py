'''
Created on 27.09.2011

@author: DuncanMCLeod
'''

import SQLs

class PyPoCaDB_Podcast():
    
    def __init__(self, _DB):
        print()
        self.mDB = _DB


    def getHighestEpisodeIDByCastID(self, castID):
        numbersQuery = self.mDB._executeCommand(SQLs.SQLs.sqlSELECTcastsAndEpisodes.format(castID))
        for number in numbersQuery:
            return number[0]


    def setHighestEpisodeIDByCastID(self, castID, episodeID):
        self.mDB._executeCommand(SQLs.SQLs.sqlUPDATEcastsAndEpisodes.format(castID, episodeID))


    def insertEpisodes(self, episodes, castID):
        ''' erwartet eine Liste von Episoden, die die Url und den Namen der Folge beinhalten, und die ID des Podcasts
        '''
        episodeID = self.getHighestEpisodeIDByCastID(castID)
        try:
            try:
                #for episode in episodes:
                anzEpisoden = len(episodes)
                while(anzEpisoden):
                    episode = episodes[anzEpisoden-1]
                    anzEpisoden = anzEpisoden-1
                    print(SQLs.SQLs.sqlINSERTepisodes.format(castID, episodeID+1, episode[0], episode[1], 1))
                    if not self.mDB._executeCommand(SQLs.SQLs.sqlINSERTepisodes.format(castID, episodeID+1, episode[0], episode[1], 1))==0:
                        episodeID = episodeID+1   # episodeID wird nur um eins erhoeht wenn die SQL-Abfrage keinen Fehler verursacht hat
                    else:
                        raise Exception()
            except:
                print("ERROR@PyPoCaDB_Podcast:insertEpisodes")
        finally:
            self.setHighestEpisodeIDByCastID(castID, episodeID)
            self.mDB.writeChanges()


    def getAllEpisodesByCastID(self, castID):
        episodesQuery = self.mDB._executeCommand(SQLs.SQLs.sqlSELECTepisodesByCast.format(castID))
        episodes = []
        for qepisode in episodesQuery:
            episode = [qepisode[0], qepisode[1], qepisode[2], qepisode[3], qepisode[4]]
            episodes.append(episode)
        return episodes
