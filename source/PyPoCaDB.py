#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import sqlite3
import Podcast
import SQLs.SQLs as SQLs

class PyPoCaDB:
    ''' dumme Klasse, sendet nur die Daten an die Datenbank wie es sie uebergeben bekommt
    '''
    def __init__(self):
        self._createStrings()
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
        self.mDBcuror = self.mDBconnection.cursor()


    def checkDB(self):
        if self.mDBopen:
            tables = self.mDBcuror.execute(SQLs.sqlgetAllTables)
            print(tables)
            print(tables.arraysize)
            if not tables.arraysize == 2:
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


    def createDB(self):
        self.createTableConfig()
        self.createTablePodcasts()
        self.createTableEpisodes()
        self.createTablepodcastsAndEpisodes()


    def createTableConfig(self):
        self._executeCommand(SQLs.sqlCREATEconfig)
        self._executeCommand(SQLs.sqlINSERTconfig_lastCastID)
        self._executeCommand(SQLs.sqlINSERTconfig_numberOfCasts)


    def createTablePodcasts(self):
        self._executeCommand(SQLs.sqlCREATEpodcasts)


    def createTableEpisodes(self):
        self._executeCommand(SQLs.sqlCREATEepisodes)


    def createTablepodcastsAndEpisodes(self):
        self._executeCommand(self.sqlCREATEcastsAndEpisodes)


    def getConfig(self, _config):
        configQuery = self._executeCommand(SQLs.sqlGETALLconfig)
        for qconfig in configQuery:
            _config[qconfig[1]] = qconfig[2] 


    def getPodcasts(self, _podcasts):
        podcastsQuery = self._executeCommand(SQLs.sqlGETALLpodcasts)
        for qpodcast in podcastsQuery:
            podcast = Podcast.Podcast(qpodcast[0])
            podcast.setName(qpodcast[1])
            podcast.setURL(qpodcast[2])
            _podcasts.add(podcast)


    def addPodcast(self, _id, _url, _name):
        self._executeCommand(SQLs.sqlINSERTpodcasts.format(_id, _url, _name))


    def updatePodcast(self, _id, _url, _name):
        self._executeCommand(SQLs.sqlUPDATEpodcasts.format(_id, _url))
        self._executeCommand(SQLs.sqlUPDATEpodcasts.format(_id, _name))


    def _executeCommand(self, command):
        try:
            try:
                return self.mDBcuror.execute(command)
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
        episodesQuery = self._executeCommand(SQLs.sqlSELECTepisodesByCast.format(castID))
        episodes = set()
        for qepisode in episodesQuery:
            episode = [qepisode[0], qepisode[1], qepisode[2], qepisode[3], qepisode[4]]
            episodes.add(episode)
        return episodes


    def insertEpisodes(self, episodes):
        ''' erwartet ein Set von Episoden
        '''
        for episode in episodes:
            self._executeCommand(SQLs.sqlINSERTepisodes.format(episode[0], episode[1], episode[2], episode[3], episode[4]))
