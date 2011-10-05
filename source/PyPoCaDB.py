#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import sqlite3
import Podcast
import SQLs

class PyPoCaDB:
    ''' dumme Klasse, sendet nur die Daten an die Datenbank wie sie sie uebergeben bekommt
    '''
    def __init__(self):
        self.mDBopen = False
        try:
            self.openDB()
            self.mDBopen = True
            self.checkDB()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            print("Fehler beim oeffnen der Datenbank")


    def openDB(self):
        self.mDBconnection = sqlite3.connect("pypoca.sqlite")
        self.mDBcursor = self.mDBconnection.cursor()


    def checkDB(self):
        if self.mDBopen:
            tables = self.mDBcursor.execute(SQLs.SQLs.sqlgetAllTables)
            print(tables)
            print(tables.arraysize)
            if not tables.arraysize == 4:
                self.mtablesArray = {'config': False, 'podcasts': False, 'episodes': False, 'podcastsAndEpisodes': False}
                for table in tables:
                    print(table)
                    self.mtablesArray[table[0]] = True
                if not self.mtablesArray['config']:
                    self.createTableConfig()
                if not self.mtablesArray['podcasts']:
                    self.createTablePodcasts()
                if not self.mtablesArray['episodes']:
                    self.createTableEpisodes()
                if not self.mtablesArray['podcastsAndEpisodes']:
                    self.createTablepodcastsAndEpisodes()
                self.writeChanges()


    def createDB(self):
        self.createTableConfig()
        self.createTablePodcasts()
        self.createTableEpisodes()
        self.createTablepodcastsAndEpisodes()
        self.writeChanges()


    def createTableConfig(self):
        self._executeCommand(SQLs.SQLs.sqlCREATEconfig)
        self._executeCommand(SQLs.SQLs.sqlINSERTconfig_lastCastID)
        self._executeCommand(SQLs.SQLs.sqlINSERTconfig_numberOfCasts)


    def createTablePodcasts(self):
        self._executeCommand(SQLs.SQLs.sqlCREATEpodcasts)


    def createTableEpisodes(self):
        self._executeCommand(SQLs.SQLs.sqlCREATEepisodes)


    def createTablepodcastsAndEpisodes(self):
        self._executeCommand(SQLs.SQLs.sqlCREATEcastsAndEpisodes)


    def getConfig(self, _config):
        configQuery = self._executeCommand(SQLs.SQLs.sqlGETALLconfig)
        for qconfig in configQuery:
            _config[qconfig[1]] = qconfig[2] 


    def getPodcasts(self, _podcasts):
        podcastsQuery = self._executeCommand(SQLs.SQLs.sqlGETALLpodcasts)
        for qpodcast in podcastsQuery:
            podcast = Podcast.Podcast(qpodcast[0], self)
            podcast.setName(qpodcast[1])
            podcast.setURL(qpodcast[2])
            _podcasts.add(podcast)


    def addPodcast(self, _id, _url, _name):
        self._executeCommand(SQLs.SQLs.sqlINSERTpodcasts.format(_id, _url, _name))


    def addEpisodeConfig(self, _castID, _episodeID):
        self.insertCastsAndEpisodes(_castID, _episodeID)


    def addEpisode(self, _episodeId, _idCast, _episodeUrl, _episodeName, _status):
        self._executeCommand(SQLs.SQLs.sqlINSERTepisodes.format(_episodeId, _idCast, _episodeUrl, _episodeName, _status))


    def updatePodcast(self, _id, _url, _name):
        self._executeCommand(SQLs.SQLs.sqlUPDATEpodcasts_url.format(_id, _url))
        self._executeCommand(SQLs.SQLs.sqlUPDATEpodcasts_name.format(_id, _name))


    def updateConfigLastCastID(self, id):
        self._executeCommand(SQLs.SQLs.sqlUPDATEconfig_lastCastID.format(id))


    def updateConfigNumberOfCasts(self, number):
        self._executeCommand(SQLs.SQLs.sqlUPDATEconfig_numberOfCasts.format(number))


    def insertCastsAndEpisodes(self, _castID, _episodeID): 
        self._executeCommand(SQLs.SQLs.sqlINSERTcastsAndEpisodes.format(_castID, _episodeID)) 


    def updateCastsAndEpisodes(self, _castID, _episodeID): 
        self._executeCommand(SQLs.SQLs.sqlUPDATEcastsAndEpisodes.format(_castID, _episodeID)) 


    def writeChanges(self):
        self.mDBconnection.commit()


    def _executeCommand(self, command):
        try:
            try:
                return self.mDBcursor.execute(command)
            except sqlite3.Error as e:
                print("PyPoCaDB@_executeCommand(self, command):")
                print("ERROR: ", e.args[0])
                print("SQL:   ", command)
        except:
            print("PyPoCaDB@_executeCommand(self, command):")
            print("ERROR: UNKNOWN")
            print("SQL:   ", command)


    def getAllEpisodes(self):
        episodesQuery = self._executeCommand("SELECT * FROM episodes")
        episodes = set()
        for qepisode in episodesQuery:
            episode = [qepisode[0], qepisode[1], qepisode[2], qepisode[3], qepisode[4]]
            episodes.add(episode)
        return episodes


    def getAllEpisodesByCastID(self, castID):
        episodesQuery = self._executeCommand(SQLs.SQLs.sqlSELECTepisodesByCast.format(castID))
        episodes = set()
        for qepisode in episodesQuery:
            episode = [qepisode[0], qepisode[1], qepisode[2], qepisode[3], qepisode[4]]
            episodes.add(episode)
        return episodes


    def insertEpisodes(self, episodes):
        ''' erwartet ein Set von Episoden
        '''
        for episode in episodes:
            self._executeCommand(SQLs.SQLs.sqlINSERTepisodes.format(episode[0], episode[1], episode[2], episode[3], episode[4]))
