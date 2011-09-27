'''
Created on 25.09.2011

@author: DuncanMCLeod
'''

import urllib
import re

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
        self.mNAME = self.getCastName(url)


    def setName(self, name):
        ''' ändert seinen Namen in 'name' um
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


    def f_urlToString(self, url):
        htmldings = urllib.request.urlopen(url);
        return str(htmldings.read().decode('utf-8'));


    def update(self):
        # catch the url
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
        print("TODO:")