#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import sqlite3
import Podcast

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
            
            
    def _createStrings(self):
        self.sqlCREATEcastsAndEpisodes = "CREATE TABLE podcastsAndEpisodes (castID INTEGER NOT NULL, highestEpisodeID INTEGER NOT NULL, UNIQUE(castid, highestEpisodeID);"
        self.sqlite3CREATEpodcasts = "CREATE TABLE podcasts (castid CONSTRAINT primkey PRIMARY KEY, castname, casturl);"
        self.sqlite3INSERTpodcasts = "INSERT INTO podcasts VALUES ({0}, {1}, {2});"
        self.sqlite3UPDATEpodcasts_name = "UPDATE podcasts SET castname='{0}' WHERE castid={1};"
        self.sqlite3UPDATEpodcasts_url  = "UPDATE podcasts SET casturl='{0}' WHERE castid={1};"
        self.sqlite3DELETEpodcasts = "DELETE FROM podcasts WHERE castid={0};"
        
        #hpodder:
        #CREATE TABLE "episodes" (castid INTEGER NOT NULL,episodeid INTEGER NOT NULL,title TEXT NOT NULL,epurl TEXT NOT NULL,enctype TEXT NOT NULL,status TEXT NOT NULL,eplength INTEGER NOT NULL DEFAULT 0,epfirstattempt INTEGER,eplastattempt INTEGER,epfailedattempts INTEGER NOT NULL DEFAULT 0,epguid TEXT,UNIQUE(castid, epurl),UNIQUE(castid, episodeid),UNIQUE(castid, epguid))
        self.sqlite3CREATEepisodes = "CREATE TABLE episodes (castid INTEGER NOT NULL, episodesid INTEGER NOT NULL, episodeURL TEXT NOT NULL, episodeNAME TEXT NOT NULL, status INT NOT NULL, UNIQUE(castid, episodeid), UNIQUE(castid, episodeURL));"
        self.sqlite3INSERTepisodes = "INSERT INTO episodes VALUES ({0}, {1}, {2}, {3}, {4});"
        self.sqlite3UPDATEepisodes_episodeURL  = "UPDATE episodes SET episodeURL='{0}' WHERE castID={1};"
        self.sqlite3UPDATEepisodes_episodeNAME = "UPDATE episodes SET episodeNAME='{0}' WHERE castID={1};"
        self.sqlite3UPDATEepisodes_status      = "UPDATE episodes SET status={0} WHERE castID={1};"
        self.sqlite3DELETEepisodes = "DELETE episodes WHERE castid={0} AND episodesid={1};"
        self.sqlite3SELECTepisodesByCast = "SELECT * FROM episodes WHERE castid={0};"

        
        
        self.sqlite3CREATEconfig = "CREATE TABLE config (confid CONSTRAINT primkey PRIMARY KEY, confname, confdata);"
        self.sqlite3INSERTconfig = "INSERT INTO config VALUES ({0}, '{1}', '{2}');"
        self.sqlite3INSERTconfig_lastCastID = self.sqlite3INSERTconfig.format(0, 'lastCastID', 0)
        self.sqlite3INSERTconfig_numberOfCasts = self.sqlite3INSERTconfig.format(1, 'numberOfCasts', 0)
        self.sqlite3getAllTables = "SELECT name, sql FROM sqlite_master WHERE type='table' ;"
        self.sqlite3GETALLpodcasts = "SELECT * from podcasts"
        self.sqlite3GETALLconfig = "SELECT * from config"


    def openDB(self):
        self.mDBconnection = sqlite3.connect("pypoca.sqlite")
        self.mDBcuror = self.mDBconnection.cursor()


    def checkDB(self):
        if self.mDBopen:
            tables = self.mDBcuror.execute(self.sqlite3getAllTables)
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
        self._executeCommand(self.sqlite3CREATEconfig)
        self._executeCommand(self.sqlite3INSERTconfig_lastCastID)
        self._executeCommand(self.sqlite3INSERTconfig_numberOfCasts)


    def createTablePodcasts(self):
        self._executeCommand(self.sqlite3CREATEpodcasts)


    def createTableEpisodes(self):
        self._executeCommand(self.sqlite3CREATEepisodes)


    def createTablepodcastsAndEpisodes(self):
        self._executeCommand(self.sqlCREATEcastsAndEpisodes)


    def getConfig(self, _config):
        configQuery = self._executeCommand(self.sqlite3GETALLconfig)
        for qconfig in configQuery:
            _config[qconfig[1]] = qconfig[2] 


    def getPodcasts(self, _podcasts):
        podcastsQuery = self._executeCommand(self.sqlite3GETALLpodcasts)
        for qpodcast in podcastsQuery:
            podcast = Podcast.Podcast(qpodcast[0])
            podcast.setName(qpodcast[1])
            podcast.setURL(qpodcast[2])
            _podcasts.add(podcast)


    def addPodcast(self, _id, _url, _name):
        self._executeCommand(self.sqlite3INSERTpodcasts.format(_id, _url, _name))


    def updatePodcast(self, _id, _url, _name):
        self._executeCommand(self.sqlite3UPDATEpodcasts.format(_id, _url))
        self._executeCommand(self.sqlite3UPDATEpodcasts.format(_id, _name))


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
        episodesQuery = self._executeCommand(self.sqlite3SELECTepisodesByCast.format(castID))
        episodes = set()
        for qepisode in episodesQuery:
            episode = [qepisode[0], qepisode[1], qepisode[2], qepisode[3], qepisode[4]]
            episodes.add(episode)
        return episodes


    def insertEpisodes(self, episodes):
        ''' erwartet ein Set von Episoden
        '''
        for episode in episodes:
            self._executeCommand(self.sqlite3INSERTepisodes.format(episode[0], episode[1], episode[2], episode[3], episode[4]))