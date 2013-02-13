'''
Created on 30.01.2013

@author: actionluzifer
'''

import os
import unittest
from source import RSS20, Podcast


class RSS20Test(unittest.TestCase):


    def setUp(self):
        self.rssTextFile = open(os.path.normpath("{0}/source/Tests/0073___das_ARD_radiofeature.xml".format(os.getcwd())), 'r')
        self.rssText = self.rssTextFile.read()
        rss = RSS20.RSS20()
        self.rssBody = rss.getRSSObject(self.rssText)
                


    def tearDown(self):
        self.rssTextFile.close()


    def test_Title(self):
        castTitle = "das ARD radiofeature"
        castName = Podcast._getCastNameByRSS(self.rssBody)
        self.assertEqual(castTitle, castName)
        
        
    def test_CastTitles(self):
        itemTitles = ("Zins und Zockerei ade","Die Spur der Keime","Der Schutzmann in Kabul",
                      "Genosse Quelle, Kamerad V-Mann","Norwegens Stunde Null","Geschäftsadresse: Gaddafi-Clan",
                      "Rechter Terror","Der Anführer","Abstellgleis für alle","Tretmühle Telekom")
        found = 0
        episodesURL = Podcast._getEpisodesByHTML(self.rssText, castID=0)
        for episode in episodesURL:
            print(episode.getName())
            if episode.getName() in itemTitles:
                found = found+1
        self.assertEqual(found, 11)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
