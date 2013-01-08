#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import sqlite3
import source.Podcast as Podcast
import source.SQLs as SQLs
import sys
import time
        
class PyPoCaDB:
    ''' dumme Klasse, sendet nur die Daten an die Datenbank wie sie sie uebergeben bekommt
    '''
    def __init__(self):
        self.mDBopen = False


    def openDB(self, dbname=":memory:"):
        self.mDBconnection = sqlite3.connect(dbname)
        self.mDBcursor = self.mDBconnection.cursor()
        self.mDBcursor.row_factory = sqlite3.Row
        result, errorMsg = self.writeCheck()
        if result < 2 or 'no such table:' in errorMsg:
            self.mDBopen = True
            if result < 1 or  'no such table:' in errorMsg:
                result = self.checkDB()

        return result


    def writeCheck(self):
        result = 0
        errorMsg = ""
        try:
            self._executeCommand(SQLs.sqlUPDATEconfig_lastused.format(int(time.time())))
            self.writeChanges()

        except sqlite3.OperationalError as e:
            errorMsg = e.args[0]
            if e.args[0] == "database is locked":
                result = 1
            else:
                result = 2

        except sqlite3.Error as e:
            errorMsg = e.args[0]
            print("An error occurred:", e.args[0])
            print("Fehler beim oeffnen der Datenbank")
            print()                    
            result = 2

        except:
            print("ERROR@PyPoCaDB::writeCheck(self):")
            exctype, value = sys.exc_info()[:2]
            print("ERROR: "+repr(exctype))
            print("       "+repr(value))
            print()
            errorMsg = exctype
            result = 2
            raise exctype

        return result, errorMsg

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
            return 0
        


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
        self._executeCommand(SQLs.sqlINSERTconfig_lastused.format(int(time.time())))


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
        longestCastName = 0
        longestCastURL = 0
        podcastsQuery = self._executeCommand(SQLs.sqlGETALLpodcasts)
        for qpodcast in podcastsQuery:
            podcast = Podcast.Podcast(qpodcast[0], self, downloadpath)
            podcast.setName(qpodcast[1])
            if len(qpodcast[1]) > longestCastName:
                longestCastName = len(qpodcast[1])
            podcast.setURL(qpodcast[2])
            if len(qpodcast[2]) > longestCastURL:
                longestCastURL = len(qpodcast[2])
            _podcasts.append(podcast)
        return longestCastName, longestCastURL


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


    def updateConfigLastCastID(self, _id):
        self._executeCommand(SQLs.sqlUPDATEconfig_lastCastID.format(_id))


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
            #try:
            self.mDBcursor.execute(command)
            return self.mDBcursor.fetchall()
        except sqlite3.Error as e:
            print("PyPoCaDB@_executeCommand(self, command):")
            print("ERROR: ", e.args[0])
            print("SQL:   ", command)
            print("type: "+str(type(command)))
            print()
            raise
        except:
            print("PyPoCaDB@_executeCommand(self, command):")
            print("ERROR: UNKNOWN")
            print("SQL:   ", command)
            print("type: "+str(type(command)))
            print()
            raise
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


    def removeAllEpisodesOfCast(self, _id):
        ''' erwartet die ID des Podcasts
        '''
        try:
            self._executeCommand(SQLs.sqlDELETEepisodesByCast.format(_id))
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@PyPoCaDB::removeAllEpisodesOfCast(self,id)")
            print("Typ:  "+repr(exctype))
            print("Wert: "+repr(value))
            print()
            return False
        return True


    def removeCast(self, _id):
        ''' erwartet die ID des Podcasts
        '''
        try:
            if not self.removeAllEpisodesOfCast(_id):
                print("Fehler: konnte nicht alle Episoden aus der Datenbank entfernen")
            self._executeCommand(SQLs.sqlDELETEcastsAndEpisodes.format(_id))
            self._executeCommand(SQLs.sqlDELETEpodcasts.format(_id))
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@PyPoCaDB::removeAllEpisodesOfCast(self,id)")
            print("Typ:  "+repr(exctype))
            print("Wert: "+repr(value))
            print()
            return False
        return True


    def updateStatusOfPodcast(self, _id, _status):
        self._executeCommand(SQLs.sqlUPDATEpodcasts_status.format(_status, _id))


    def renamePodcast(self, _podcastID, _newName):
        self._executeCommand(SQLs.sqlUPDATEpodcasts_name.format(_newName, _podcastID))


    def changeURLofPodcast(self, _podcastID, _newURL):
        self._executeCommand(SQLs.sqlUPDATEpodcasts_url.format(_newURL, _podcastID))


    def updateConfig(self, lastCastID, numberOfCasts):
        print()
        self.updateConfigLastCastID(lastCastID)
        self.updateConfigNumberOfCasts(numberOfCasts)
