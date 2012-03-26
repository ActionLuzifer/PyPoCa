#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import PyPoCaDB
import Podcast
#from Podcast.Podcast import Podcast as Podcast
#from Downloader.Intern import Intern as DownIntern
import os
import re
import RSS20
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
                        self.STR_basepath:self.getDownloadpathInConfig()}
        self.mDB.getConfig(self.mConfig)
        for config in self.mConfig:
            print(config+" - "+str(self.mConfig[config]))
            
        # Podcasts
        self.mPodcasts = list()
        self.mDB.getPodcasts(self.mPodcasts, self.mConfig[self.STR_basepath])


    def saveConfig(self):
        print()
        self.mDB.updateConfig(self.mConfig[self.STR_lastCastID], self.mConfig[self.STR_numberOfCasts])
        self.mDB.writeChanges()
        


    def getIDofPodcast(self, _name):
        for podcast in self.mPodcasts:
            if podcast.getName() == _name:
                return podcast.getID()


    def addPodcast(self, name, _url):
        try:
            # allgemeine Daten holen
            castID = int(self.mConfig[self.STR_lastCastID]) + 1
            numberofcasts = int(self.mConfig[self.STR_numberOfCasts]) + 1
            
            # Podcast-spezifische Daten erstellen
            podcast = Podcast.Podcast(castID, self.mDB, self.mConfig[self.STR_basepath])
            podcast.updateName(name)
            
            # Podcast-spezifische Daten in die DB schreiben
            self.mDB.addPodcast(castID, podcast.getName(), _url, 1)
            self.mDB.addEpisodeConfig(castID, 0)
            
            # allgemeine Daten in die DB schreiben
            self.mDB.updateConfigLastCastID(castID)
            self.mDB.updateConfigNumberOfCasts(numberofcasts)
        
            self.mConfig[self.STR_lastCastID] = str(castID)
            self.mConfig[self.STR_numberOfCasts] = str(numberofcasts)
            self.mDB.writeChanges()
        except:
            print("ERROR@PyPoCa::addPodcast(self, _url)")
            exctype, value = sys.exc_info()[:2]
            print("ERROR: "+repr(exctype))
            print("       "+repr(value))
            raise exctype

        return podcast


    def addPodcastByURL(self, _url):
        rss = RSS20.RSS20()
        rssBody = rss.getRSSObject(Podcast.f_urlToString(_url))
        name =  Podcast._getCastNameByRSS(rssBody)
        self.addPodcast(name, _url)


    def addPodcastByFile(self, _path):
        _url = os.path.normpath(_path)
        rss = RSS20.RSS20()
        rssBody = rss.getRSSObject(Podcast.f_fileToString(_url))
        name =  Podcast._getCastNameByRSS(rssBody)
        self.addPodcast(name, _path)


    def removePodcastByID(self, _id):
        if not self.mDB.removeCast(_id):
            print("Fehler: konnte den Podcast NICHT korrekt aus der Datenbank entfernen!")
        else:
            self.mDB.writeChanges()


    def enablePodcastByID(self, _id):
        ''' enables the podcast with this ID '''
        self.mDB.updateStatusOfPodcast(_id, 1)
        self.mDB.writeChanges()

        
    def disablePodcastByID(self, _id):
        ''' disables the podcast with this ID '''
        self.mDB.updateStatusOfPodcast(_id, 0)
        self.mDB.writeChanges()

        
    def update(self):
        for podcast in self.mPodcasts:
            print("podcast.getStatus(): "+repr(podcast.getStatus()))
            if int(podcast.getStatus())==1:
                podcast.update(False)


    def download(self):
        for podcast in self.mPodcasts:
            status = int(podcast.getStatus())
            if status==1:
                podcast.download("intern")


    def list(self):
        anzahlStellen=len(repr(len(self.mPodcasts)))
        formatStr = "{:0>"+repr(anzahlStellen)+"}"
        for podcast in self.mPodcasts:
            try:
                print(formatStr.format(repr(podcast.getID()))+"  |  "+podcast.getName() + "  |  "+podcast.getURL())
            except:
                print("Problem bei der Darstellung von einem Podcast")


    def getDownloadpathInConfig(self):
        # Datei einlesen
        myfileName = os.path.normpath("{0}/config.xml".format(os.getcwd()))
        myfile = open(myfileName, 'r')
        result = myfile.read()
        myfile.close()
        
        # Ausdruck finden
        bigRE = "(.)*<downloadpath>(?P<DownloadPath>(.)*)</downloadpath>(.)*";
        REprogramm = re.compile(bigRE);
        foundObject = REprogramm.search(result);
        result = foundObject.group("DownloadPath")
        
        return result


    def printVersion(self):
        print("0.0.1.1")
        
        
    def rsstest(self):
        rssHtml = Podcast.f_urlToString("http://www.dradio.de/rss/podcast/sendungen/breitband")
        rss = RSS20.RSS20()
        rss.getRSSObject(rssHtml)


    def printHelp(self):
        self.printVersion()
        print("Usage: pypoca [options [sub-options]]\n\
 -h, --help     Displays this help message\n\
 -v, --version  Displays the current version\n\
 update         updates all enabled podcasts from it sources (internet or file)\n\
 download       download new episodes of all enabled podcasts\n\
 list           shows all podcasts\n\
 (list OPTION   shows all podcasts) not yet implemented\n\
 add URL        add a new podcast from internet (per http(s))\n\
 addf FILE      add a new podcast from a file\n\
 removeI ID     removes the podcast with this ID\n\
 removeN NAME   remove the podcast with this NAME\n\
 enable ID      enables the podcast with this ID\n\
 disable ID     disables the podcast with this ID")
