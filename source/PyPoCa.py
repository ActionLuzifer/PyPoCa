#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
    
    stdout_encoding = sys.stdout.encoding or sys.getfilesystemencoding()
    
    def __init__(self, configxml=os.path.normpath("{0}/config.xml".format(os.getcwd()))):
        self.STR_CONFIG_RegExTemplateKey = "$KEY"
        self.STR_CONFIG_RegExTemplate = "(.)*<"+self.STR_CONFIG_RegExTemplateKey+">(?P<"+self.STR_CONFIG_RegExTemplateKey+">(.)*)</"+self.STR_CONFIG_RegExTemplateKey+">(.)*"
        self.STR_configxmlFilename = configxml
        self.STR_lastCastID = 'lastCastID'
        self.STR_numberOfCasts = 'numberOfCasts'
        self.STR_basepath = 'downloadpath'


    def _openDatabase(self, dbname):
        self.mDB = PyPoCaDB.PyPoCaDB(dbname)


    def loadConfig(self):
        # Config
        self._openDatabase(self.getDBnameInConfig())
        self.mConfig = {self.STR_lastCastID:"0", 
                        self.STR_numberOfCasts:"0",
                        self.STR_basepath:self.getDownloadpathInConfig()}
        self.mDB.getConfig(self.mConfig)
        for config in self.mConfig:
            print(str(config)+" - "+str(self.mConfig[config]))
            
        # Podcasts
        self.mPodcasts = list()
        self.mDB.getPodcasts(self.mPodcasts, self.mConfig[self.STR_basepath])
        


    def saveConfig(self):
        print()
        self.mDB.updateConfig(self.mConfig[self.STR_lastCastID], self.mConfig[self.STR_numberOfCasts])
        self.mDB.writeChanges()
        

    def getPodcastByID(self, castID):
        result = False
        for podcast in self.mPodcasts:
            if int(podcast.getID()) == int(castID):
                result = podcast
                break
        return result


    def getIDofPodcast(self, _name):
        for podcast in self.mPodcasts:
            if podcast.getName() == _name:
                return podcast.getID()


    def addPodcast(self, name, _url):
        try:
            # allgemeine Daten holen
            castID = int(self.mConfig[self.STR_lastCastID]) + 1
            numberofcasts = int(self.mConfig[self.STR_numberOfCasts]) + 1
            
            # Podcast-spezifische Daten in die DB schreiben
            self.mDB.addPodcast(castID, name, _url, 1)
            self.mDB.addEpisodeConfig(castID, 0)
            
            # Podcast-spezifische Daten erstellen
            podcast = Podcast.Podcast(castID, self.mDB, self.mConfig[self.STR_basepath])
            podcast.updateName(name)
            
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
        rssString, isRSSstringOK = Podcast.f_urlToString(_url)
        if isRSSstringOK:
            rssBody = rss.getRSSObject(rssString)
            name = Podcast._getCastNameByRSS(rssBody)
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
            if int(podcast.getStatus())==1:
                try:
                    self.printPodcastName(podcast)
                    podcast.update(False)
                except:
                    print("Ups")

        
    def updateID(self, castID):
        podcast = self.getPodcastByID(castID)
        if podcast:
            self.printPodcastName(podcast)
            podcast.update(False)


    def download(self):
        for podcast in self.mPodcasts:
            status = int(podcast.getStatus())
            if status==1:
                print()
                podcast.printName()
                podcast.download("intern")


    def downloadID(self, castID):
        podcast = self.getPodcastByID(castID)
        if podcast:
            self.printPodcastName(podcast)
            podcast.download("intern")


    def list(self):
        anzahlStellen=len(repr(len(self.mPodcasts)))
        formatStr = "{:0>"+repr(anzahlStellen)+"}"
        for podcast in self.mPodcasts:
            try:
                print(formatStr.format(repr(podcast.getID()))+"  |  "+podcast.getName().encode(self.stdout_encoding, 'ignore').decode('utf-8','ignore')+ "  |  "+podcast.getURL()) 
            except:
                print("Problem bei der Darstellung von einem Podcast")


    def getConfigfileStr(self):
        # Datei einlesen
        myfileName = self.STR_configxmlFilename
        myfile = open(myfileName, 'r')
        result = myfile.read()
        myfile.close()
        return result


    def getFindRegEx(self, searchstring, regexstring, groupname):
        REprogramm = re.compile(regexstring);
        foundObject = REprogramm.search(searchstring);
        return foundObject.group(groupname)
    
    
    def getDBnameInConfig(self):
        result = self.getConfigfileStr()
        
        # Ausdruck finden
        key = "dbName"
        return self.getFindRegEx(result, self.STR_CONFIG_RegExTemplate.replace(self.STR_CONFIG_RegExTemplateKey, key), key)


    def getDownloadpathInConfig(self):
        result = self.getConfigfileStr()
        
        # Ausdruck finden
        key = "downloadpath"
        return self.getFindRegEx(result, self.STR_CONFIG_RegExTemplate.replace(self.STR_CONFIG_RegExTemplateKey, key), key)


    def printVersion(self):
        print("0.0.1.7")
        
        
    def rsstest(self):
        rssHtml = Podcast.f_urlToString("http://www.dradio.de/rss/podcast/sendungen/breitband")
        rss = RSS20.RSS20()
        rss.getRSSObject(rssHtml)


    def printPodcastName(self, podcast):
        try:
            anzahlStellen=len(repr(len(self.mPodcasts)))
            formatStr = "{:0>"+repr(anzahlStellen)+"}"
            print(formatStr.format(repr(podcast.getID()))+"  |  "+podcast.getName().encode(self.stdout_encoding, 'ignore').decode('utf-8','ignore')) 
        except:
            print("Problem bei der Darstellung von einem Podcast")


    def printHelp(self):
        self.printVersion()
        print("Usage: pypoca [options [sub-options]]\n\
 -h, --help     Displays this help message\n\
 -v, --version  Displays the current version\n\
 update         updates all enabled podcasts from it sources (internet or file)\n\
 updateID       updates the podcast with the given ID from it source\n\
 download       download new episodes of all enabled podcasts\n\
 downloadID     download new episodes of the podcast with the given ID\n\
 list           shows all podcasts\n\
 (list OPTION   shows all podcasts) not yet implemented\n\
 add URL        add a new podcast from internet (per http(s))\n\
 addf FILE      add a new podcast from a file\n\
 removeI ID     removes the podcast with this ID\n\
 removeN NAME   remove the podcast with this NAME\n\
 enable ID      enables the podcast with this ID\n\
 disable ID     disables the podcast with this ID")
