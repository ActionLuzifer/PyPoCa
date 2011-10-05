'''
Created on 25.09.2011

@author: DuncanMCLeod
'''

import urllib
import re
import io
import os

class Podcast:
    '''
    classdocs
    '''


    def __init__(self, ID, DB):
        '''
        Constructor
        '''
        self.mDB = DB
        self.mID = ID
        self.mNAME = ""
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
        episodesDB = self.mDB.getAllEpisodesByCastID()
        # getEpisodesFromURL
        episodesURL = self.getEpisodesByHTML(htmlpage)
        # make a diff
        newEpisodes = self.getNewEpisodes(episodesDB, episodesURL)
        # send new episodes to DB
        self.mDB.insertEpisodes(newEpisodes)


    def getEpisodesByHTML(self, htmlpage):
        ''' zieht aus der html-datei die einzelnen Episoden-Urls
        '''
        print("TODO:")
        
    def getNewEpisodes(self, episodesDB, episodesURL):
        ''' Zieht die Episoden aus der episodesURL ab die bereits in der episodesDB
            vorhanden sind.
        '''
        print("TODO:")
        