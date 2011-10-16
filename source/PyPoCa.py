#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import PyPoCaDB
import Podcast
import os
import sys

class PyPoCa:
    def __init__(self):
        self.STR_lastCastID = 'lastCastID'
        self.STR_numberOfCasts = 'numberOfCasts'
        self.STR_basepath = "downloadpath"


    def _openDatabase(self):
        self.mDB = PyPoCaDB.PyPoCaDB()


    def loadConfig(self):
        # Config
        self._openDatabase()
        self.mConfig = {self.STR_lastCastID:0, 
                        self.STR_numberOfCasts:0, 
                        self.STR_basepath:os.path.normpath(sys.argv[0])}
        self.mDB.getConfig(self.mConfig)
        for config in self.mConfig:
            print(config+" - "+str(self.mConfig[config]))
            
        # Podcasts
        self.mPodcasts = set()
        self.mDB.getPodcasts(self.mPodcasts, self.mConfig[self.STR_basepath])
        for podcast in self.mPodcasts:
            print(podcast.getName())


    def addPodcast(self, _url):
        try:
            castID = self.mConfig[self.STR_lastCastID] +1 
            podcast = Podcast(castID, self.mDB)
            podcast.updateNameByURL(url=_url)
            self.mDB.addPodcast(castID, _url, podcast.getName())
            self.mConfig[self.STR_lastCastID] + 1
        except:
            print("ERROR@PyPoCa::addPodcast(self, _url)")
            print(os.error)


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
            podcast.download("intern")


    def list(self):
        anzahlStellen=len(repr(len(self.mPodcasts)))
        formatStr = "{:0>"+repr(anzahlStellen)+"}"
        for podcast in self.mPodcasts:
            print(formatStr.format(repr(podcast.getID()))+"  |  "+podcast.getName())


    def printVersion(self):
        print("0.0.6")


    def printHelp(self):
        self.printVersion()
        print("Usage: pypoca [options [sub-options]] \n\
 -h, --help     Displays this help message \n\
 -v, --version  Displays the current version \n\
 update         updates all enabled podcasts from it sources (internet or file)\n\
 download       download new episodes of all enabled podcasts \n\
 list           shows all podcasts \n\
 (list OPTION   shows all podcasts) not yet implemented \n\
 add URL        add a new podcast from internet (per http(s)) \n\
 addf FILE      add a new podcast from a file \n\
 (remove ID     removes the podcast with this ID) not yet implemented \n\
 (remove NAME   remove the podcast with this NAME) not yet implemented \n\
 (enable ID     enables the podcast with this ID) not yet implemented \n\
 (enable NAME   enables the podcast with this NAME) not yet implemented \n\
 (disable ID    disables the podcast with this ID) not yet implemented \n\
 (disable NAME  disables the podcast with this NAME) not yet implemented")
