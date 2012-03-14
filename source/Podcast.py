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
import RSS20
import Episode


def f_decodeCastReader(reader):
    alreadyread = reader.read()
    readString = str(alreadyread)
    if('encoding="ISO-8859-1"' in readString):
        decodedStr = alreadyread.decode('iso-8859-1', errors='ignore')
    elif('encoding="utf-8"' in readString):
        decodedStr = alreadyread.decode('utf_8', errors='ignore')
    else:
        print("UNKNOWN ENCODING!!!")
        decodedStr = readString
    return decodedStr


def f_urlToString(url):
    htmldings = urllib.request.urlopen(url);
    return f_decodeCastReader(htmldings);


def _getCastName(htmlstring):
    bigRE = "(.)*<title( )*>(?P<CastTitle>(.)*)</title( )*>(.)*";
    REprogramm = re.compile(bigRE);
    foundObject = REprogramm.search(htmlstring);
    castNAME = foundObject.group("CastTitle")
    return castNAME


def _getCastNameByURL(url):
    htmlpage = f_urlToString(url)
    print("htmlpage: "+htmlpage)
    return _getCastName(htmlpage)


def _getCastNameByFile(url):
    htmlpage = f_fileToString(url)
    return _getCastName(htmlpage)


def f_fileToString(file):
    castreader = io.FileIO(file)
    caststring = f_decodeCastReader(castreader)
    return caststring


class Podcast:
    '''
    classdocs
    '''


    def __init__(self, ID, DB, downloadPath):
        '''
        Constructor
        '''

        print("MOIN")        
        self.mDB = PyPoCaDB_Podcast.PyPoCaDB_Podcast(DB)
        print("MOINMOIN")
        ''' CAST-ID '''
        self.mID = ID
        self.mDownloadPathBase = downloadPath
        self.reloadData()


    def reloadData(self):
        try:
            cast = self.mDB.getPodcastInfosByCastID(self.mID)
        except:
            cast = False
        if cast:        
            ''' CAST-Name '''
            self.mNAME = cast["castname"]
        
            ''' CAST-URL '''
            self.mURL = cast["casturl"]
            
            self.mStatus = cast["status"]
            
            self.mDownloadPath = os.path.normpath(self.mDownloadPathBase+"/" +self.mNAME)
        else:
            self.mNAME = ""
            self.mURL = ""            
            self.mStatus = 1


    def updateName(self, name):
        self.mNAME = name


    def updateNameByURL(self, url):
        ''' holt sich die html-seite und benennt sich nach dem '<title>'-Tag um
            ausserdem speichert sich der Podcast die neue 'url'
        '''
        self.mURL = url
        self.mNAME = _getCastNameByURL(url)

    def updateNameByFile(self, url):
        self.mURL = url
        self.mNAME = _getCastNameByFile(url)


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


    def update(self, byFile):
        # catch the url
        htmlpage = ""
        if byFile:
            htmlpage = self.f_fileToString(os.path.normpath("C:\\Office\\arbeit\\pypoca\\Doc\\podcasts\\Breitband-feed.xml"))
        else:
            htmlpage = f_urlToString(self.mURL)

        # getEpisodesFromDB
        episodesDB = self.mDB.getAllEpisodesByCastID(self.mID)
        # getEpisodesFromURL
        episodesURL = self.getEpisodesByHTML(htmlpage)
        # make a diff
        newEpisodes = self.getNewEpisodes(episodesDB, episodesURL)
        # send new episodes to DB
        if ( len(newEpisodes)>0 ):
            self.mDB.insertEpisodes(newEpisodes, self.mID)


    def getEpisodesByHTML(self, htmlpage):
        ''' zieht aus der html-datei die einzelnen Episoden-Urls
        '''
        episoden = []
        
        rss = RSS20.RSS20()
        rssBody = rss.getRSSObject(htmlpage)
        
        channelItem = rssBody.getItemWithName("channel")
        if channelItem:
            items = channelItem.getSubitemsWithName("item")
            for rssitem in items:
                titleitem = rssitem.getSubitemWithName("title")
                linkitem  = rssitem.getSubitemWithName("link")
                guiditem  = rssitem.getSubitemWithName("guid")
                if guiditem is False:
                    guiditem = linkitem
                if (titleitem) and (linkitem):
                    episode = Episode.Episode(self.mID, -1, linkitem.getContent(), 
                                              titleitem.getContent(), guiditem.getContent(), SQLs.episodestatus["new"])
                    episoden.insert(0, episode)
        
        return episoden


    def getNewEpisodes(self, episodesDB, episodesURL):
        ''' Zieht die Episoden aus der episodesURL ab die bereits in der episodesDB
            vorhanden sind.
        '''
        if len(episodesDB):
            newEpisodes = []
            
            for episodeurl in episodesURL:
                found = False
                for episodedb in episodesDB:
                    if episodeurl.episodeGUID == episodedb.episodeGUID:
                        found = True
                        break 
                if not found:
                    newEpisodes.insert(0,episodeurl)
        else:
            newEpisodes = episodesURL
        return newEpisodes


    def download(self, downloadMethod):
        print("TODO")
        if self.checkDownloadPath():
            episoden = self.mDB.getAllEpisodesByCastID(self.mID)
            for episode in episoden:
                print(episode)
                if not episode.episodeStatus == SQLs.episodestatus["downloaded"]:
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
                            self.mDB.writeChanges()
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
        if (episode.episodeStatus==SQLs.episodestatus["new"]):
            str = "{:0>4}".format(episode.episodeID)
            # TODO: Dateiendung ermitteln und an castFileName anhaengen
            castFileName = os.path.normpath("{0}/{1}_-_{2}".format(self.mDownloadPath,str,episode.episodeName))
            print("castFileName: "+castFileName)
            downloader.download(episode.episodeID, castFileName, episode.episodeURL, episode.episodeStatus)


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


if __name__ == '__main__':
    import sys
    sys.path.append("/home/actionluzifer/Dokumente/sourcen/workspace/pypoca")
    files=os.listdir("/home/actionluzifer/Dokumente/sourcen/workspace/pypoca")
    for file in files:
        if ("start.py" in file):
            file = file.replace(".py", "")
            pluginImport = __import__(file, globals(), locals(), [], 0)
            pluginImport.starten()