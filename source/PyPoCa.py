#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created on 2011-09-24

@author: actionluzifer
'''

import source.PyPoCaDB as PyPoCaDB
import source.Podcast as Podcast
#from Podcast.Podcast import Podcast as Podcast
#from Downloader.Intern import Intern as DownIntern
import os
import re
import source.RSS20 as RSS20
import sys


class PyPoCa:
    
    stdout_encoding = sys.stdout.encoding or sys.getfilesystemencoding()
    
    def __init__(self, configxml=os.path.normpath("{0}/config.xml".format(os.getcwd()))):
        self.check4configfile(configxml)
        self.STR_CONFIG_RegExTemplateKey = "$KEY"
        self.STR_CONFIG_RegExTemplate = "(.)*<"+self.STR_CONFIG_RegExTemplateKey+">(?P<"+self.STR_CONFIG_RegExTemplateKey+">(.)*)</"+self.STR_CONFIG_RegExTemplateKey+">(.)*"
        self.STR_configxmlFilename = configxml
        self.STR_lastCastID = 'lastCastID'
        self.STR_numberOfCasts = 'numberOfCasts'
        self.STR_basepath = 'downloadpath'
        self.STR_lastused = 'lastused'
        self.longestCastName = 1
        self.longestCastURL = 1


    def check4configfile(self, configxml):
        if os.path.exists(configxml):
            return
        newfile = open(configxml, 'w')
        newfile.write("<downloadpath>podcasts</downloadpath>\r\n")
        newfile.write("<dbName>pypoca.sqlite</dbName>\r\n")
        newfile.close()


    def _openDatabase(self, dbname):
        self.mDB = PyPoCaDB.PyPoCaDB()
        return self.mDB.openDB(dbname)


    def loadConfig(self):
        result = self._openDatabase(self.getDBnameInConfig())
        self.mPodcasts = list()
        if result < 2:
            # Config
            self.mConfig = {self.STR_lastCastID:"0", 
                            self.STR_numberOfCasts:"0",
                            self.STR_basepath:self.getDownloadpathInConfig(),
                            self.STR_lastused:"0"}
            self.mDB.getConfig(self.mConfig)
            
            # Podcasts
            self.longestCastName, self.longestCastURL = self.mDB.getPodcasts(self.mPodcasts, self.mConfig[self.STR_basepath])
        else:
            self.longestCastName = 1
            self.longestCastURL = 1

        return result


    def saveConfig(self):
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
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                raise
            
            # wenn keine Fehler kamen, dann bitte jetzt in DB schreiben
            self.mDB.writeChanges()
        except:
            print("ERROR@PyPoCa::addPodcast(self, _url)")
            exctype, value = sys.exc_info()[:2]
            print("ERROR: "+repr(exctype))
            print("       "+repr(value))
            raise exctype

        return podcast


    def addPodcastByURL(self, _url):
        try:
            rss = RSS20.RSS20()
            rssString, isRSSstringOK = Podcast.f_urlToString(_url)
            if isRSSstringOK:
                rssBody = rss.getRSSObject(rssString)
                name = Podcast._getCastNameByRSS(rssBody)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            raise 
        if isRSSstringOK:
            self.addPodcast(name, _url)


    def addPodcastByFile(self, _path):
        try:
            _url = os.path.normpath(_path)
            rss = RSS20.RSS20()
            rssBody = rss.getRSSObject(Podcast.f_fileToString(_url))
            name =  Podcast._getCastNameByRSS(rssBody)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            raise
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


    def renamePodcast(self, _podcastID, _newName):
        ''' renames the podcast with this ID '''
        podcast = self.getPodcastByID(_podcastID)
        podcast.setName(_newName)
        self.mDB.renamePodcast(_podcastID, _newName)
        self.mDB.writeChanges() 


    def changeURLofPodcast(self, _podcastID, _newURL):
        ''' changes the URL of the podcast with this ID '''
        podcast = self.getPodcastByID(_podcastID)
        podcast.setURL(_newURL)
        self.mDB.changeURLofPodcast(_podcastID, _newURL)
        self.mDB.writeChanges()


    def update(self, podcast):
        try:
            podcast.printName()
            podcast.update(False)
            self.mDB.writeChanges()
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@PyPoCa::update(self, podcast)")
            print("Typ:  "+repr(exctype))
            print("Wert: "+repr(value))
            print()

    def updateAll(self):
        try:
            for podcast in self.mPodcasts:
                if int(podcast.getStatus())==1:
                    self.update(podcast)
        except (KeyboardInterrupt, SystemExit):
            raise


    def updateID(self, castID):
        try:
            podcast = self.getPodcastByID(castID)
            if podcast:
                self.update(podcast)
        except (KeyboardInterrupt, SystemExit):
            raise


    def download(self, podcast):
        podcast.printName()
        return podcast.download("intern")


    def downloadAll(self):
        downloadedEpisodes = []
        try:
            for podcast in self.mPodcasts:
                status = int(podcast.getStatus())
                if status==1:
                    tmpDownloadedEpisodes = self.download(podcast)
                    for episode in tmpDownloadedEpisodes:
                        downloadedEpisodes.append(episode)
        except (KeyboardInterrupt, SystemExit):
            raise
        return downloadedEpisodes
                        


    def downloadID(self, castID):
        downloadedEpisodes = []
        try:
            podcast = self.getPodcastByID(castID)
            if podcast:
                downloadedEpisodes = self.download(podcast)
        except (KeyboardInterrupt, SystemExit):
            raise
        return downloadedEpisodes



    def showList(self):
        try:
            anzahlStellen=len(repr(len(self.mPodcasts)))
            if self.longestCastURL < len("Url"):
                self.longestCastURL = len("Url")
            if self.longestCastName < len("Name"):
                self.longestCastName = len("Name")
            print("| {0:>{1}}".format("ID", anzahlStellen)
                  +" |{0:>{1}}".format(" Stat", 1)
                  +"| {0:{1}}".format("Name", self.longestCastName)
                  +" | {0:{1}}".format("URL", self.longestCastURL)+" | ")
            print("|-{0:->{1}}".format("--", anzahlStellen)
                  +"-|{0:->{1}}".format("-----", 1)
                  +"|-{0:->{1}}".format("----", self.longestCastName)
                  +"-|-{0:->{1}}".format("----", self.longestCastURL)+" | ")
            #print("{0:#>{1}}".format("", anzahlStellen+self.longestCastName+self.longestCastURL))
            for podcast in self.mPodcasts:
                try:
                    print("| {0:>{1}}".format(repr(podcast.getID()), anzahlStellen)
                          +" |  {0:>{1}}".format(podcast.getStatusStr(), 1)
                          +"  | {0:{1}}".format(podcast.getName().encode(self.stdout_encoding, 'ignore').decode('utf-8','ignore'), self.longestCastName)
                          +" | {0:{1}}".format(podcast.getURL(), self.longestCastURL)+" | ") 
                except:
                    print("Problem bei der Darstellung von einem Podcast")
        except (KeyboardInterrupt, SystemExit):
            raise


    def showListEpisodes(self):
        try:
            anzahlStellen=len(repr(len(self.mPodcasts)))
            if self.longestCastURL < len("Url"):
                self.longestCastURL = len("Url")
            if self.longestCastName < len("Name"):
                self.longestCastName = len("Name")
            print("| {0:>{1}}".format("ID", anzahlStellen)
                  +" |{0:>{1}}".format(" Stat", 1)
                  +"| {0:{1}}".format("Name", self.longestCastName)
                  +" | {0:{1}}".format("URL", self.longestCastURL)+" | ")
            print("|-{0:->{1}}".format("--", anzahlStellen)
                  +"-|{0:->{1}}".format("-----", 1)
                  +"|-{0:->{1}}".format("----", self.longestCastName)
                  +"-|-{0:->{1}}".format("----", self.longestCastURL)+" | ")
            #print("{0:#>{1}}".format("", anzahlStellen+self.longestCastName+self.longestCastURL))
            for podcast in self.mPodcasts:
                try:
                    print("| {0:>{1}}".format(repr(podcast.getID()), anzahlStellen)
                          +" |  {0:>{1}}".format(podcast.getStatusStr(), 1)
                          +"  | {0:{1}}".format(podcast.getName().encode(self.stdout_encoding, 'ignore').decode('utf-8','ignore'), self.longestCastName)
                          +" | {0:{1}}".format(podcast.getURL(), self.longestCastURL)+" | ")
                    for episode in podcast.getEpisodes():
                        try:
                            episode.printName()
                        except:
                            print("Problem bei der Darstellung einer Episode")
                except:
                    print("Problem bei der Darstellung von einem Podcast")
                    print("ERROR@PyPoCa::showListEpisodes(self)")
                    exctype, value = sys.exc_info()[:2]
                    print("ERROR: "+repr(exctype))
                    print("       "+repr(value))
        except (KeyboardInterrupt, SystemExit):
            raise


    def getConfigfileStr(self):
        # Datei einlesen
        try:
            myfileName = self.STR_configxmlFilename
            myfile = open(myfileName, 'r')
            result = myfile.read()
        finally:
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
        print("0.0.2.0")
        
        
    def rsstest(self):
        rssHtml, allright = Podcast.f_urlToString("http://feeds.feedburner.com/wrint/wrint")
        #rssHtml = Podcast.f_urlToString("http://www.dradio.de/rss/podcast/sendungen/breitband")
        if allright:
            rss = RSS20.RSS20()
            rssobject = rss.getRSSObject(rssHtml)
            rss.debugItem2(rssobject)


    def getPlaylistFilename(self):
        import time
        now    = time.localtime()
        nowStr = "{:0>4}-{:0>2}-{:0>2}_{:0>2}-{:0>2}-{:0>2}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        return os.path.normpath("{0}/{1}.m3u".format(self.mConfig[self.STR_basepath], nowStr))


    def writePlaylist(self, downloadedEpisodes, playlistname):
        file = open(playlistname, 'a')
        for episode in downloadedEpisodes:
            file.write(episode+"\n")
        file.close()
        print("Playlist geschrieben: "+playlistname)
        

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
 remove ID      removes the podcast with this ID\n\
 (removeN NAME  remove the podcast with this NAME) not yet implemented\n\
 enable ID      enables the podcast with this ID\n\
 disable ID     disables the podcast with this ID")
