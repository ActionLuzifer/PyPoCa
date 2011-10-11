'''
Created on 25.09.2011

@author: DuncanMCLeod
'''

import urllib
import re
import io
import os
import PyPoCaDB_Podcast

class Podcast:
    '''
    classdocs
    '''


    def __init__(self, ID, DB):
        '''
        Constructor
        '''
        
        self.mDB = PyPoCaDB_Podcast.PyPoCaDB_Podcast(DB)
         
        ''' CAST-ID '''
        self.mID = ID
        
        ''' CAST-Name '''
        self.mNAME = ""
        
        ''' CAST-URL '''
        self.mURL = ""


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
        episoden = self.mDB.getAllEpisodesByCastID(self.mID)
        for episode in episoden:
            print(episode)
            if downloadMethod=="wget":
                self.downloadEpisodePerWget(episode)
            elif downloadMethod=="curl":
                self.downloadEpisodePerCurl(episode)
            elif downloadMethod=="intern":
                self.downloadEpisodePerIntern(episode)


    def downloadEpisodePerWget(self, episode):
        print("TODO")


    def downloadEpisodePerCurl(self, episode):
        print("TODO")


    def downloadEpisodePerIntern(self, episode):
        print("TODO")

        