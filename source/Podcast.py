'''
Created on 25.09.2011

@author: DuncanMCLeod
'''

import re
import io
import os
import PyPoCaDB_Podcast
import urllib.request
import SQLs
from Downloader.Intern import Intern as DownIntern

class Podcast:
    '''
    classdocs
    '''


    def __init__(self, ID, DB, downloadPath):
        '''
        Constructor
        '''
        
        self.mDB = PyPoCaDB_Podcast.PyPoCaDB_Podcast(DB)
        ''' CAST-ID '''
        self.mID = ID
        self.mDownloadPathBase = downloadPath
        self.reloadData()


    def reloadData(self):
        cast = self.mDB.getPodcastInfosByCastID(self.mID)
        if cast:        
            ''' CAST-Name '''
            self.mNAME = cast["castname"]
        
            ''' CAST-URL '''
            self.mURL = cast["casturl"]
            
            self.mStatus = cast["status"]
            
            self.mDownloadPath = os.path.normpath(self.mDownloadPathBase+"\\" +self.mNAME)
        else:
            self.mNAME = ""
            self.mURL = ""            
            self.mStatus = 1


    def updateName(self):
        self.updateNameByURL(self.mURL)


    def updateNameByURL(self, url):
        ''' holt sich die html-seite und benennt sich nach dem '<title>'-Tag um
            ausserdem speichert sich der Podcast die neue 'url'
        '''
        self.mURL = url
        self.mNAME = self._getCastName(url)

    def updateNameByFile(self, url):
        self.mURL = url
        self.mNAME = self._getCastNameByFile(url)


    def getID(self):
        return self.mID


    def setName(self, name):
        ''' aendert seinen Namen in "name" um
        '''
        self.mNAME = name


    def getName(self):
        return self.mNAME


    def setURL(self, url):
        self.mURL = url


    def getURL(self):
        return self.mURL
    
    
    def setStatus(self, _status):
        self.mStatus = _status
        
    
    def getStatus(self):
        return self.mStatus


    def _getCastName(self, url):
        htmlpage = self.f_urlToString(url)
        bigRE = "(.)*<title>(?P<CastTitle>(.)*)</title>(.)*";
        REprogramm = re.compile(bigRE);
        foundObject = REprogramm.search(htmlpage);
        castNAME = foundObject.group("CastTitle")
        return castNAME


    def _getCastNameByFile(self, url):
        htmlpage = self.f_fileToString(url)
        bigRE = "(.)*<title>(?P<CastTitle>(.)*)</title>(.)*";
        REprogramm = re.compile(bigRE);
        foundObject = REprogramm.search(htmlpage);
        castNAME = foundObject.group("CastTitle")
        return castNAME



    def f_urlToString(self, url):
        htmldings = urllib.request.urlopen(url);
        #return str(htmldings.read().decode('ISO-8859-1'));
        return self.f_decodeString(str(htmldings.read()));


    def f_fileToString(self, file):
        castreader = io.FileIO(file)
        #caststring = castreader.read().decode('utf-8')
        caststring = self.f_decodeString(castreader.read())
        return caststring


    def f_decodeString(self, string):
        try:
            return string.decode('utf-8')
        except:
            try:
                return string.decode('ISO-8859-1')
            except:
                print("error")


    def update(self):
        # catch the url
        htmlpage = ""
        byFile = True
        if byFile:
            htmlpage = self.f_fileToString(os.path.normpath("C:\\Office\\arbeit\\pypoca\\Doc\\podcasts\\Breitband-feed.xml"))

        else:
            htmlpage = self.f_urlToString(self.mURL)

        # getEpisodesFromDB
        episodesDB = self.mDB.getAllEpisodesByCastID(self.mID)
        # getEpisodesFromURL
        episodesURL = self.getEpisodesByHTML(htmlpage)
        # make a diff
        newEpisodes = self.getNewEpisodes(episodesDB, episodesURL)
        # send new episodes to DB
        self.mDB.insertEpisodes(newEpisodes, self.mID)


    def getEpisodesByHTML(self, htmlpage):
        ''' zieht aus der html-datei die einzelnen Episoden-Urls
        '''
        linkList = []
        
        # um den einzelnen Cast zu identifizieren
        castRE = "<item>*"
        castREprog = re.compile(castRE)
        
        # um den Link fuer die Episode zu identifizieren
        linkRE = "(.)*<link>(?P<link>(.)*)</link>(.)*"
        linkREprog = re.compile(linkRE)
        
        nameRE = "(.)*<title>(?P<name>(.)*)</title>(.)*"
        nameREprog = re.compile(nameRE)
        
        for foundSomething in castREprog.split(htmlpage):
            if re.search("(.)*</item>(.)*", foundSomething):
                foundLink = linkREprog.search(foundSomething)
                if foundLink:
                    foundName = nameREprog.search(foundSomething)
                    link = [foundLink.group("link"), foundName.group("name")]
                    linkList.append(link)
        return linkList


    def getNewEpisodes(self, episodesDB, episodesURL):
        ''' Zieht die Episoden aus der episodesURL ab die bereits in der episodesDB
            vorhanden sind.
        '''
        if len(episodesDB):
            newEpisodes = []
            
            for episodeurl in episodesURL:
                found = False
                for episodedb in episodesDB:
                    print(episodeurl[0])
                    print(episodedb[2])
                    if episodeurl[0] == episodedb[2]:
                        found = True
                        break 
                if not found:
                    newEpisodes.append(episodeurl)
        else:
            newEpisodes = episodesURL
        return newEpisodes


    def download(self, downloadMethod):
        print("TODO")
        if self.checkDownloadPath():
            episoden = self.mDB.getAllEpisodesByCastID(self.mID)
            for episode in episoden:
                print(episode)
                if not episode[4] == SQLs.episodestatus["downloaded"]:
                    try:                        
                        try:
                            if downloadMethod=="wget":
                                downloader = False
                            elif downloadMethod=="curl":
                                downloader = False                                
                            elif downloadMethod=="intern":
                                downloader = DownIntern(self)
                                
                            self.downloadEpisode(downloader, episode)
                        finally:
                            self.mDB.updateEpisodeStatus(episode, "downloaded")
                    except urllib.error.URLError as e:
                        print("Podcast@download(self, downloadMethod):")
                        print("ERROR: ", e.args[0])
                        print("method:   ", downloadMethod)
                        try:
                            self.mDB.updateEpisodeStatus(episode, "error")
                        except:
                            print("ERROR: can't write ERROR to Database")
            self.mDB.writeChanges()
                    

    def downloadEpisode(self, downloader, episode):
        str = "{:0>4}".format(episode[1])
        castFileName = os.path.normpath("{0}/{1}_-_{2}".format(self.mDownloadPath,str,episode[3]))
        downloader.download(episode[1], castFileName, episode[2], episode[4])


    def checkDownloadPath(self):
        try:
            if not os.path.exists(self.mDownloadPath):
                os.makedirs(self.mDownloadPath)
        except OSError as e:
                print("Podcast@checkDownloadPath(self):")
                print("ERROR: ", e.args[0])
                print("PATH:   ", self.mDownloadPath)
                return 0
        return 1
