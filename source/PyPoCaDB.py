#!/usr/bin/python3

"""
Created on 2011-09-24

@author: actionluzifer
"""

import sqlite3
import source.Podcast as Podcast
import source.SQLs as SQLs
import sys
import time
        
class PyPoCaDB:
    """ dumme Klasse, sendet nur die Daten an die Datenbank wie sie sie uebergeben bekommt
    """
    def __init__(self):
        self.mDBopen = False
        self.mDBconnection = None
        self.mDBcursor = None



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
            self.executeCommand(SQLs.sqlUPDATEconfig_lastused, (int(time.time()),), True)
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
            raise exctype

        return result, errorMsg

    def checkDB(self):
        if self.mDBopen:
            tablesC = self.mDBcursor.execute(SQLs.sqlgetAllTables)
            tables = tablesC.fetchall()
                
            if not len(tables) == 4:
                mtablesArray = {'config': False, 'podcasts': False, 'episodes': False, 'podcastsAndEpisodes': False}
                for table in tables:
                    print(table[0])
                    mtablesArray[table[0]] = True
                if not mtablesArray['config']:
                    self.createTableConfig()
                if not mtablesArray['podcasts']:
                    self.createTablePodcasts()
                if not mtablesArray['episodes']:
                    self.createTableEpisodes()
                if not mtablesArray['podcastsAndEpisodes']:
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
        self.executeCommand(SQLs.sqlCREATEconfig)
        self.executeCommand(SQLs.sqlINSERTconfig_lastCastID)
        self.executeCommand(SQLs.sqlINSERTconfig_numberOfCasts)
        self.executeCommand(SQLs.sqlINSERTconfig_lastused, (int(time.time()),), True)


    def createTablePodcasts(self):
        self.executeCommand(SQLs.sqlCREATEpodcasts)


    def createTableEpisodes(self):
        self.executeCommand(SQLs.sqlCREATEepisodes)


    def createTablepodcastsAndEpisodes(self):
        self.executeCommand(SQLs.sqlCREATEcastsAndEpisodes)


    def getConfig(self, _config):
        configQuery = self.executeCommand(SQLs.sqlGETALLconfig)
        for qconfig in configQuery:
            _config[qconfig[1]] = qconfig[2]


    def getPodcasts(self, downloadpath, showError):
        podcasts = list()
        longestCastName = 0
        longestCastURL = 0
        podcastsQuery = self.executeCommand(SQLs.sqlGETALLpodcasts)
        for qpodcast in podcastsQuery:
            podcast = Podcast.Podcast(qpodcast[0], self, downloadpath, showError)
            podcast.setName(qpodcast[1])
            if len(qpodcast[1]) > longestCastName:
                longestCastName = len(qpodcast[1])
            podcast.setURL(qpodcast[2])
            if len(qpodcast[2]) > longestCastURL:
                longestCastURL = len(qpodcast[2])
            podcasts.append(podcast)
        return longestCastName, longestCastURL, podcasts


    def addPodcast(self, _id, _name, _url, _status):
        self.executeCommand(SQLs.sqlINSERTpodcasts, (_id, _name, _url, _status), True)


    def addEpisodeConfig(self, _castID, _episodeID):
        self.insertCastsAndEpisodes(_castID, _episodeID)


    def addEpisode(self, _episodeId, _idCast, _episodeUrl, _episodeName, _episodeGUID, _status):
        self.executeCommand(SQLs.sqlINSERTepisodes, (_episodeId, _idCast, _episodeUrl, _episodeName, _episodeGUID, _status), True)


    def updatePodcast(self, _id, _url, _name, _status):
        self.executeCommand(SQLs.sqlUPDATEpodcasts_url, (_id, _url), True)
        self.executeCommand(SQLs.sqlUPDATEpodcasts_name, (_id, _name), True)
        self.executeCommand(SQLs.sqlUPDATEpodcasts_status, (_id, _status), True)


    def updateConfigLastCastID(self, _id):
        self.executeCommand(SQLs.sqlUPDATEconfig_lastCastID, (_id,), True)


    def updateConfigNumberOfCasts(self, number):
        self.executeCommand(SQLs.sqlUPDATEconfig_numberOfCasts, (number,), True)


    def insertCastsAndEpisodes(self, _castID, _episodeID): 
        self.executeCommand(SQLs.sqlINSERTcastsAndEpisodes, (_castID, _episodeID), True)


    def updateCastsAndEpisodes(self, _castID, _episodeID): 
        self.executeCommand(SQLs.sqlUPDATEcastsAndEpisodes, (_castID, _episodeID), True)


    def writeChanges(self):
        self.mDBconnection.commit()


    def executeCommand(self, command, args=None, hasArgs=False):
        try:
            if hasArgs:
                self.mDBcursor.execute(command, (args,))
            else:
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


    def getAllEpisodes(self):
        episodesQuery = self.executeCommand("SELECT * FROM episodes")
        episodes = set()
        for qepisode in episodesQuery:
            episode = [qepisode[0], qepisode[1], qepisode[2], qepisode[3], qepisode[4], qepisode[5]]
            episodes.add(episode)
        return episodes


    def insertEpisodes(self, episodes):
        """ erwartet ein Set von Episoden
        """
        for episode in episodes:
            self.executeCommand(SQLs.sqlINSERTepisodes, (episode[0], episode[1], episode[2], episode[3], episode[4], episode[5]), True)


    def removeAllEpisodesOfCast(self, _id):
        """ erwartet die ID des Podcasts
        """
        try:
            self.executeCommand(SQLs.sqlDELETEepisodesByCast, (_id,), True)
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@PyPoCaDB::removeAllEpisodesOfCast(self,id)")
            print("Typ:  "+repr(exctype))
            print("Wert: "+repr(value))
            print()
            return False
        return True


    def removeCast(self, _id):
        """ erwartet die ID des Podcasts
        """
        try:
            if not self.removeAllEpisodesOfCast(_id):
                print("Fehler: konnte nicht alle Episoden aus der Datenbank entfernen")
            self.executeCommand(SQLs.sqlDELETEcastsAndEpisodes, (_id,), True)
            self.executeCommand(SQLs.sqlDELETEpodcasts, (_id,), True)
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@PyPoCaDB::removeAllEpisodesOfCast(self,id)")
            print("Typ:  "+repr(exctype))
            print("Wert: "+repr(value))
            print()
            return False
        return True


    def updateStatusOfPodcast(self, _id, _status):
        self.executeCommand(SQLs.sqlUPDATEpodcasts_status, (_status, _id), True)


    def renamePodcast(self, _podcastID, _newName):
        self.executeCommand(SQLs.sqlUPDATEpodcasts_name, (_newName, _podcastID), True)


    def changeURLofPodcast(self, _podcastID, _newURL):
        self.executeCommand(SQLs.sqlUPDATEpodcasts_url, (_newURL, _podcastID), True)


    def updateConfig(self, lastCastID, numberOfCasts):
        print()
        self.updateConfigLastCastID(lastCastID)
        self.updateConfigNumberOfCasts(numberOfCasts)
