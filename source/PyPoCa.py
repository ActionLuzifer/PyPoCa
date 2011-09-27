#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import PyPoCaDB
import Podcast

class PyPoCa:
    def __init__(self):
        self.STR_lastCastID = 'lastCastID'
        self.STR_numberOfCasts = 'numberOfCasts'
        self._openDatabase()


    def update(self):
        for podcast in self.mPodcasts:
            print("TODO:")


    def _openDatabase(self):
        self.mDB = PyPoCaDB.PyPoCaDB()


    def loadConfig(self):
        self.mPodcasts = set()
        self.mDB.getPodcasts(self.mPodcasts)
        for podcast in self.mPodcasts:
            print(podcast)
        self.mConfig = {self.STR_lastCastID:0, self.STR_numberOfCasts:0}
        self.mDB.getConfig(self.mConfig)
        for config in self.mConfig:
            print(config+" - "+self.mConfig[config])


    def addPodcast(self, _url):
        castID = self.mConfig[self.STR_lastCastID] =+ 1
        podcast = Podcast(castID, self.mDB)
        podcast.updateNameByURL(url=_url)
        self.mDB.addPodcast(castID, _url, podcast.getName())

    def updatePodcasts(self):
        for podcast in self.mPodcasts:
            podcast.update()