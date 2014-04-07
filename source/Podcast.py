# -*- coding: utf-8 -*-
'''
Created on 25.09.2011

@author: DuncanMCLeod
'''

import io
import os
import source.PyPoCaDB_Podcast as PyPoCaDB_Podcast
import urllib.request
import source.SQLs as SQLs
from source.Downloader.Intern import Intern as DownIntern
import source.RSS20 as RSS20
import source.Episode as Episode
import source.public_functions as public_functions
import time, sys


def f_decodeCastReader(reader):
    alreadyread = reader.read()
    readString = str(alreadyread)
    if('encoding="ISO-8859-1"' in readString) or (('encoding="iso-8859-1"' in readString)):
        decodedStr = alreadyread.decode('iso-8859-1', errors='ignore')
    elif('encoding="utf-8"' in readString) or ('encoding="UTF-8"' in readString):
        decodedStr = alreadyread.decode('utf_8', errors='ignore')
    else:
        print("UNKNOWN ENCODING!!!")
        decodedStr = readString
    return decodedStr


def f_urlToString(url):
    try:
        htmldings = urllib.request.urlopen(url)
        return f_decodeCastReader(htmldings), True
    except:
        return "", False


def _getCastName(htmlstring):
    rss = RSS20.RSS20()
    rssBody = rss.getRSSObject(htmlstring)
    
    channelItem = rssBody.getItemWithName("channel")
    if channelItem:
        item = channelItem.getSubitemWithName("title")
        if (item):
            print(item.getContent())
            return item.getContent()


def _getCastNameByRSS(rssBody):
    if (rssBody != False):
        channelItem = rssBody.getItemWithName("channel")
        if channelItem:
            item = channelItem.getSubitemWithName("title")
            if item:
                name = public_functions.f_replaceBadCharsByRegEx(item.getContent())
                print(name)
                return name
    else:
        return ""


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


def _getEpisodesByHTML(htmlpage, castID):
    ''' zieht aus der html-datei die einzelnen Episoden-Urls
    '''
    episoden = []
    
    rss = RSS20.RSS20()
    rssBody = rss.getRSSObject(htmlpage)
    
    channelItem = rssBody.getItemWithName("channel")
    if channelItem:
        items = channelItem.getSubitemsWithName("item")
        for rssitem in items:
            titleitem     = rssitem.getSubitemWithName("title")
            enclosureitem = rssitem.getSubitemWithName("enclosure")
            guiditem      = rssitem.getSubitemWithName("guid")
            pubDateItem   = rssitem.getSubitemWithName("pubDate")
            if pubDateItem:
                pubDate = getEpisodeTime(pubDateItem.getContent())
            else:
                pubDate = time.gmtime(0)
            if enclosureitem:
                linkitem = enclosureitem.getSubitemWithName("url")
                if guiditem is False:
                    guiditem = linkitem
                if titleitem and linkitem:
                    episode = Episode.Episode(castID, -1, linkitem.getContent(), public_functions.f_replaceBadCharsByRegEx(titleitem.getContent()), 
                                              guiditem.getContent(), SQLs.episodestatus["new"], pubDate)
                    episoden.insert(0, episode)
    
    return episoden
    
    
def getEpisodeTime(timeStr):
    try:
        mytime = time.strptime(timeStr[:-6], "%a, %d %b %Y %H:%M:%S")
    except:
        try:
            mytime = time.strptime(timeStr[:-4], "%a, %d %b %Y %H:%M:%S")
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR@Podcast:getEpisodeTime(timeStr)")
            print("Typ:  "+repr(exctype))
            print("Wert: "+repr(value))
            print("Time: ",timeStr)
            print()
            mytime = time.gmtime(0)
    return mytime
        

def getKey(episode):
        return episode.pubDate



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
        self.mDownloadPathBase = downloadPath[:3] + public_functions.f_replaceBadCharsPath(downloadPath[3:])
        self.reloadData()


    def reloadData(self):
        try:
            cast = self.mDB.getPodcastInfosByCastID(self.mID)
        except:
            cast = False
            print("ERROR@Podcast::reloadData: castID=="+repr(self.mID))
        if cast:        
            ''' CAST-Name '''
            self.mNAME = cast["castname"]
        
            ''' CAST-URL '''
            self.mURL = cast["casturl"]
            
            self.mStatus = cast["status"]
            
            self.mDownloadPath = os.path.normpath(self.mDownloadPathBase+"/" +public_functions.f_replaceBadCharsPath(self.mNAME))
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


    def getStatusStr(self):
        result = ""
        if self.mStatus == 0:
            result = "-"
        elif self.mStatus == 1:
            result = "+"
        else:
            result = "?"
        return result


    def update(self, byFile):
        # catch the url
        htmlpage = ""
        isHTML = False
        if byFile:
            htmlpage = self.f_fileToString(self.mURL)
            isHTML = True
        else:
            htmlpage, isHTML = f_urlToString(self.mURL)

        if isHTML:
            # getEpisodesFromDB
            episodesDB = self.mDB.getAllEpisodesByCastID(self.mID)
            # getEpisodesFromURL
            episodesURL = _getEpisodesByHTML(htmlpage, self.mID)

            
            self.sortEpisodes(episodesURL)

            # check for new or changed episodes
            changedEpisodes, newEpisodes = self.getChangedAndNewEpisodes(episodesDB, episodesURL)
            
            # Update Episodes
            if len(changedEpisodes)>0:
                for newEpisode in changedEpisodes:
                    oldEpisode = self.getEpisodeByGUID(newEpisode.episodeGUID)
                    if oldEpisode is not None:
                        if newEpisode.episodeURL != oldEpisode.episodeURL:
                            self.mDB.updateEpisodeURL(self.getID(), oldEpisode.episodeID, newEpisode.episodeURL)  
                        if newEpisode.episodeName != oldEpisode.episodeName:
                            self.mDB.updateEpisodeName(self.getID(), oldEpisode.episodeID, newEpisode.episodeName)
                self.mDB.writeChanges()

            # send new episodes to DB
            if ( len(newEpisodes)>0 ):
                print("--> +",len(newEpisodes)," Episoden")
                for episode in newEpisodes:
                    print("----> ",episode.episodeName)
                self.mDB.insertEpisodes(newEpisodes, self.mID)


    def getEpisodes(self):
        return self.mDB.getAllEpisodesByCastID(self.mID)
    
    
    def getEpisodeByGUID(self, _GUID):
        result = None
        for episode in self.getEpisodes():
            if episode.episodeGUID == _GUID:
                result = episode
                break
        return result


    def sortEpisodes(self, episodes):
        episodes.sort(key=getKey)
        return episodes


    def getChangedAndNewEpisodes(self, episodesDB, episodesURL):
        ''' gleicht die vorhandenen Episoden mit denen vom Feed auf Änderungen ab '''
        changedEpisodes = []
        newEpisodes = []
        if len(episodesDB):
            for episodeurl in episodesURL:
                found = False
                changed = False
                for episodedb in episodesDB:
                    if (episodeurl.episodeGUID == episodedb.episodeGUID):
                        found = True
                        if episodeurl.episodeURL != episodedb.episodeURL:
                            changed = True
                        if episodeurl.episodeName != episodedb.episodeName:
                            changed = True
                        break 
                if changed:
                    changedEpisodes.insert(0,episodeurl)
                if not found:
                    newEpisodes.insert(0, episodeurl)

        # Listen sortieren
        if len(changedEpisodes)>0:
            changedEpisodes = self.sortEpisodes(changedEpisodes)
        if len(newEpisodes)>0:
            newEpisodes = self.sortEpisodes(newEpisodes)
        
        return changedEpisodes, newEpisodes


    def download(self, downloadMethod):
        downloadedEpisodes = []
        if self.checkDownloadPath():
            try:
                episoden = self.mDB.getAllEpisodesByCastID(self.mID)
                for episode in episoden:
                    isError = False
                    if ((episode.episodeStatus == SQLs.episodestatus["new"]) or
                        (episode.episodeStatus == SQLs.episodestatus["error"]) or  
                        (episode.episodeStatus == SQLs.episodestatus["incomplete"])):
                        try:                        
                            try:
                                if downloadMethod=="wget":
                                    downloader = False
                                elif downloadMethod=="curl":
                                    downloader = False                                
                                elif downloadMethod=="intern":
                                    downloader = DownIntern(self)
                                    
                                isError, statuscode, castFileNames = self.downloadEpisode(downloader, episode)
                            finally:
                                if not isError:
                                    self.mDB.updateEpisodeStatus(episode, "downloaded")
                                    downloadedEpisodes.append(castFileNames)
                                else:
                                    if statuscode == 404 or statuscode == "404":
                                        self.mDB.updateEpisodeStatus(episode, "404")
                                    else:
                                        self.mDB.updateEpisodeStatus(episode, "error")
                                self.mDB.writeChanges()
                        except (KeyboardInterrupt, SystemExit):
                            self.mDB.updateEpisodeStatus(episode, "incomplete")
                            raise
                        except urllib.error.URLError as e:
                            print("Podcast@download(self, downloadMethod):")
                            print("ERROR: ", e.args[0])
                            print("method:   ", downloadMethod)
                            try:
                                self.mDB.updateEpisodeStatus(episode, "error")
                            except:
                                print("ERROR: can't write ERROR to Database")
            except (KeyboardInterrupt, SystemExit):
                self.mDB.writeChanges()
                raise
                    
            self.mDB.writeChanges()
            return downloadedEpisodes


    def getFileExtension(self, url):
        foundAt = url.rfind(".")
        if foundAt > 0:
            result = url[foundAt:len(url)]
            return result
        else:
            return ""


    def downloadEpisode(self, downloader, episode):
        eID = "{:0>4}".format(episode.episodeID)
        castFileName = os.path.normpath("{0}/{1}_-_{2}".format(self.mDownloadPath,eID,public_functions.f_replaceBadCharsFiles(episode.episodeName+self.getFileExtension(episode.episodeURL))))
        episode.printName()
        isError, statuscode = downloader.download(episode.episodeID, castFileName, episode.episodeURL, episode.episodeStatus)
        return isError, statuscode, castFileName


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


    def printName(self):
        try:
            eID = "{:0>4}".format(self.getID())
            try:
                print("Cast: ", eID, " | ", self.getName())
            except: 
                print("Cast: ", eID, " | ", self.getName().encode(self.stdout_encoding, 'ignore').decode('utf-8','ignore')) 
        except:
            print("Problem bei der Darstellung von dem Podcast")
