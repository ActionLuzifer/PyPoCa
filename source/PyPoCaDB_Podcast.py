'''
Created on 27.09.2011

@author: DuncanMCLeod
'''

import PyPoCaDB
import SQLs.SQLs as SQLs

class PyPoCaDB_Podcast():
    
    def __init__(self, _DB):
        print()
        self.mDB = _DB
        self.mDBcursor = self.mDB.cursor()


    def insertEpisodes(self, episodes):
        ''' erwartet ein Set von Episoden
        '''
        for episode in episodes:
            self.mDB._executeCommand(SQLs.sqlINSERTepisodes.format(episode[0], episode[1], episode[2], episode[3], episode[4]))