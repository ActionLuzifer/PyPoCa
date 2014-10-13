"""
Created on 05.11.2011

@author: DuncanMCLeod
"""

class Downloader:
    """Basisklasse fuer den Downloadprozess"""


    def __init__(self, podcastObj=None, anzahlThreads=1):
        """ Constructor """
        self.podcastObj     = podcastObj    # hierher koennen Statusaenderungen der jeweiligen Episode geschickt werden
        self.anzahlThreads  = anzahlThreads


    def download(self, id, castFileName, url, status):
        pass
