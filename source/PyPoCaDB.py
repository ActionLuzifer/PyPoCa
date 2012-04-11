#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import sqlite3
import Podcast
import SQLs
import sys

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
        self.mDBcursor.row_factory = sqlite3.Row


    def checkDB(self):
        if self.mDBopen:
            tablesC = self.mDBcursor.execute(SQLs.sqlgetAllTables)
            tables = tablesC.fetchall()
                
            if not len(tables) == 4:
                self.mtablesArray = {'config': False, 'podcasts': False, 'episodes': False, 'podcastsAndEpisodes': False}
                for table in tables:
                    print(table[0])
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
        self._executeCommand(SQLs.sqlCREATEconfig)
        self._executeCommand(SQLs.sqlINSERTconfig_lastCastID)
        self._executeCommand(SQLs.sqlINSERTconfig_numberOfCasts)


    def createTablePodcasts(self):
        self._executeCommand(SQLs.sqlCREATEpodcasts)


    def createTableEpisodes(self):
        self._executeCommand(SQLs.sqlCREATEepisodes)


    def createTablepodcastsAndEpisodes(self):
        self._executeCommand(SQLs.sqlCREATEcastsAndEpisodes)


    def getConfig(self, _config):
        configQuery = self._executeCommand(SQLs.sqlGETALLconfig)
        for qconfig in configQuery:
            _config[qconfig[1]] = qconfig[2]


    def getPodcasts(self, _podcasts, downloadpath):
        podcastsQuery = self._executeCommand(SQLs.sqlGETALLpodcasts)
        for qpodcast in podcastsQuery:
            podcast = Podcast.Podcast(qpodcast[0], self, downloadpath)
            podcast.setName(qpodcast[1])
            podcast.setURL(qpodcast[2])
            _podcasts.append(podcast)


    def addPodcast(self, _id, _name, _url, _status):
        self._executeCommand(SQLs.sqlINSERTpodcasts.format(_id, _name, _url, _status))


    def addEpisodeConfig(self, _castID, _episodeID):
        self.insertCastsAndEpisodes(_castID, _episodeID)


    def addEpisode(self, _episodeId, _idCast, _episodeUrl, _episodeName, _episodeGUID, _status):
        self._executeCommand(SQLs.sqlINSERTepisodes.format(_episodeId, _idCast, _episodeUrl, _episodeName, _episodeGUID, _status))


    def updatePodcast(self, _id, _url, _name, _status):
        self._executeCommand(SQLs.sqlUPDATEpodcasts_url.format(_id, _url))
        self._executeCommand(SQLs.sqlUPDATEpodcasts_name.format(_id, _name))
        self._executeCommand(SQLs.sqlUPDATEpodcasts_status.format(_id, _status))


    def updateConfigLastCastID(self, id):
        self._executeCommand(SQLs.sqlUPDATEconfig_lastCastID.format(id))


    def updateConfigNumberOfCasts(self, number):
        self._executeCommand(SQLs.sqlUPDATEconfig_numberOfCasts.format(number))


    def insertCastsAndEpisodes(self, _castID, _episodeID): 
        self._executeCommand(SQLs.sqlINSERTcastsAndEpisodes.format(_castID, _episodeID)) 


    def updateCastsAndEpisodes(self, _castID, _episodeID): 
        self._executeCommand(SQLs.sqlUPDATEcastsAndEpisodes.format(_castID, _episodeID)) 


    def writeChanges(self):
        self.mDBconnection.commit()


    def _executeCommand(self, command):
        try:
            try:
                self.mDBcursor.execute(command)
                return self.mDBcursor.fetchall()
            except sqlite3.Error as e:
                print("PyPoCaDB@_executeCommand(self, command):")
                print("ERROR: ", e.args[0])
                print("SQL:   ", command)
                print("type: "+str(type(command)))
                return 0
        except:
            print("PyPoCaDB@_executeCommand(self, command):")
            print("ERROR: UNKNOWN")
            print("SQL:   ", command)
            print("type: "+str(type(command)))
            return 2
        return 0


    def getAllEpisodes(self):
        episodesQuery = self._executeCommand("SELECT * FROM episodes")
        episodes = set()
        for qepisode in episodesQuery:
            episode = [qepisode[0], qepisode[1], qepisode[2], qepisode[3], qepisode[4], qepisode[5]]
            episodes.add(episode)
        return episodes


    def insertEpisodes(self, episodes):
        ''' erwartet ein Set von Episoden
        '''
        for episode in episodes:
            self._executeCommand(SQLs.sqlINSERTepisodes.format(episode[0], episode[1], episode[2], episode[3], episode[4], episode[5]))


    def removeAllEpisodesOfCast(self, id):
        ''' erwartet die ID des Podcasts
        '''
        try:
            self._executeCommand(SQLs.sqlDELETEepisodesByCast.format(id))
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@PyPoCaDB::removeAllEpisodesOfCast(self,id)")
            print("Typ:  "+exctype)
            print("Wert: "+value)
            return False
        return True


    def removeCast(self, id):
        ''' erwartet die ID des Podcasts
        '''
        try:
            if not self.removeAllEpisodesOfCast(id):
                print("Fehler: konnte nicht alle Episoden aus der Datenbank entfernen")
            self._executeCommand(SQLs.sqlDELETEcastsAndEpisodes.format(id))
            self._executeCommand(SQLs.sqlDELETEpodcasts.format(id))
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@PyPoCaDB::removeAllEpisodesOfCast(self,id)")
            print("Typ:  "+exctype)
            print("Wert: "+value)
            return False
        return True


    def updateStatusOfPodcast(self, _id, _status):
        self._executeCommand(SQLs.sqlUPDATEpodcasts_status.format(_status, _id))


    def updateConfig(self, lastCastID, numberOfCasts):
        print()
        self.updateConfigLastCastID(lastCastID)
        self.updateConfigNumberOfCasts(numberOfCasts)
