#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import sys
sys.path.append("source");
import PyPoCa


def starten():
    pypoca = PyPoCa.PyPoCa()
    anzArguments = len(sys.argv)
    if (anzArguments > 1):
        i = 0
        pypoca.loadConfig()
        while not i == anzArguments-1:
            i+=1
            commandStr = sys.argv[i]
            print(anzArguments)
            print(commandStr)
            if commandStr=="update":
                pypoca.updateAll()
            if commandStr=="updateID":
                if anzArguments > i+1:
                    pypoca.updateID(sys.argv[i+1])
                    i+=1
            elif commandStr=="download":
                downloadedEpisodes = pypoca.downloadAll()
                for episode in downloadedEpisodes:
                    print(episode)
                pypoca.writePlaylist(downloadedEpisodes, pypoca.getPlaylistFilename())
            elif commandStr=="downloadID":
                if anzArguments > i+1:
                    downloadedEpisodes = pypoca.downloadID(sys.argv[i+1])
                    for episode in downloadedEpisodes:
                        print(episode)

                pypoca.writePlaylist(downloadedEpisodes, pypoca.getPlaylistFilename())

                i+=1
            elif commandStr=="add":
                pypoca.addPodcastByURL(sys.argv[i+1])
                pypoca.saveConfig()
            elif commandStr=="addf":
                pypoca.addPodcastByFile(sys.argv[i+1])
                pypoca.saveConfig()
            elif commandStr=="remove":
                pypoca.removePodcastByID(sys.argv[i+1])
                pypoca.saveConfig()
            elif commandStr=="enable":
                pypoca.enablePodcastByID(sys.argv[i+1])
            elif commandStr=="disable":
                pypoca.disablePodcastByID(sys.argv[i+1])
            elif commandStr=="--version" or commandStr=="-v":
                pypoca.printVersion()
            elif commandStr=="--help" or commandStr=="-h":
                pypoca.printHelp()
            elif commandStr=="list":
                pypoca.showList()
            elif commandStr=="rss":
                pypoca.rsstest()
    else:
        pypoca.showList()


if __name__ == '__main__':
    starten()
