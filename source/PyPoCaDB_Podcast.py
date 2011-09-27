'''
Created on 27.09.2011

@author: DuncanMCLeod
'''

import PyPoCaDB

class PyPoCaDB_Podcast():
    
    def __init__(self, _DB):
        print()
        self.mDB = _DB
        self.mDBcuror = self.mDB.cursor()
        self.sqlINSERTcastsAndEpisodes = "INSERT INTO podcastsAndEpisodes VALUES ({0}, {1});"
        self.sqlUPDATEcastsAndEpisodes = "UPDATE podcastsAndEpisodes SET highestEpisodeID={0} WHERE castID={1};"
        self.sqlDELETEcastsAndEpisodes = "DELETE podcastsAndEpisodes WHERE castid={0}"


    def insertEpisodes(self, episodes):
        ''' erwartet ein Set von Episoden
        '''
        for episode in episodes:
            self.mDB._executeCommand(self.sqlite3INSERTepisodes.format(episode[0], episode[1], episode[2], episode[3], episode[4]))