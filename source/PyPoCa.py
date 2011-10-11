#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import PyPoCaDB
import Podcast
import os

class PyPoCa:
    def __init__(self):
        self.STR_lastCastID = 'lastCastID'
        self.STR_numberOfCasts = 'numberOfCasts'
        self._openDatabase()


    def _openDatabase(self):
        self.mDB = PyPoCaDB.PyPoCaDB()


    def loadConfig(self):
        self.mPodcasts = set()
        self.mDB.getPodcasts(self.mPodcasts)
        for podcast in self.mPodcasts:
            print(podcast.getName())
        self.mConfig = {self.STR_lastCastID:0, self.STR_numberOfCasts:0}
        self.mDB.getConfig(self.mConfig)
        for config in self.mConfig:
            print(config+" - "+str(self.mConfig[config]))


    def addPodcast(self, _url):
        castID = self.mConfig[self.STR_lastCastID] =+ 1
        podcast = Podcast(castID, self.mDB)
        podcast.updateNameByURL(url=_url)
        self.mDB.addPodcast(castID, _url, podcast.getName())


    def addPodcastByFile(self):
        # allgemeine Daten holen
        castID = int(self.mConfig[self.STR_lastCastID]) + 1 
        numberofcasts = int(self.mConfig[self.STR_numberOfCasts]) + 1
        
        
        # Podcast-spezifische Daten holen
        podcast = Podcast.Podcast(castID, self.mDB)
        _url = os.path.normpath("C:\\Office\\arbeit\\pypoca\\Doc\\podcasts\\Breitband-feed.xml")
        podcast.updateNameByFile(_url)
        
        # Podcast-spezifische Daten in die DB schreiben
        self.mDB.addPodcast(castID, podcast.getName(), _url)
        self.mDB.addEpisodeConfig(castID, 0)
        
        # allgemeine Daten in die DB schreiben
        self.mDB.updateConfigLastCastID(castID)
        self.mDB.updateConfigNumberOfCasts(numberofcasts)
        
        # allgemeine Daten im RAM updaten
        self.mConfig[self.STR_lastCastID] = castID
        self.mConfig[self.STR_numberOfCasts] = numberofcasts
        self.mDB.writeChanges()


    def update(self):
        for podcast in self.mPodcasts:
            podcast.update()


    def download(self):
        for podcast in self.mPodcasts:
            podcast.download()
