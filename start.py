#!/usr/bin/python3
# coding=utf-8
'''
Created on 2011-09-24

@author: actionluzifer
'''

import sys
import source.PyPoCa as PyPoCa


def starten():
    pypoca = PyPoCa.PyPoCa()
    anzArguments = len(sys.argv)
    print("anzArguments: "+str(anzArguments))
    print()
    if (anzArguments > 1):
        i = 0
        dbstatus = pypoca.loadConfig()
        while not i == anzArguments-1:
            i+=1
            commandStr = sys.argv[i]
            print("commandStr:   "+str(commandStr))
            print()
            if dbstatus < 1:
                # db is fine
                if commandStr=="update":
                    pypoca.updateAll()
                    continue
                if commandStr=="updateID":
                    if anzArguments > i+1:
                        pypoca.updateID(sys.argv[i+1])
                        i+=1
                    continue
                elif commandStr=="download":
                    downloadedEpisodes = pypoca.downloadAll()
                    pypoca.writePlaylist(downloadedEpisodes, pypoca.getPlaylistFilename())
                    continue
                elif commandStr=="downloadID":
                    if anzArguments > i+1:
                        downloadedEpisodes = pypoca.downloadID(sys.argv[i+1])
                        pypoca.writePlaylist(downloadedEpisodes, pypoca.getPlaylistFilename())
                    i+=1
                    continue
                elif commandStr=="add":
                    pypoca.addPodcastByURL(sys.argv[i+1])
                    i+=1
                    pypoca.saveConfig()
                    continue
                elif commandStr=="addf":
                    continue
                    pypoca.addPodcastByFile(sys.argv[i+1])
                    i+=1
                    pypoca.saveConfig()
                    continue
                elif commandStr=="remove":
                    pypoca.removePodcastByID(sys.argv[i+1])
                    i+=1
                    pypoca.saveConfig()
                    continue
                elif commandStr=="enable":
                    pypoca.enablePodcastByID(sys.argv[i+1])
                    i+=1
                    continue
                elif commandStr=="disable":
                    pypoca.disablePodcastByID(sys.argv[i+1])
                    i+=1
                    continue
                elif commandStr=="rename":
                    pypoca.renamePodcast(sys.argv[i+1], sys.argv[i+2])
                    i+=2
                    continue
                elif commandStr=="changeURL":
                    pypoca.changeURLofPodcast(sys.argv[i+1], sys.argv[i+2])
                    i+=2
                    continue

            if dbstatus < 2:
                if commandStr=="--version" or commandStr=="-v":
                    pypoca.printVersion()
                    continue
                elif commandStr=="--help" or commandStr=="-h":
                    pypoca.printHelp()
                    continue
                elif commandStr=="list":
                    pypoca.showList()
                    continue
                elif commandStr=="listEpisodes":
                    pypoca.showListEpisodes()
                    continue
                elif commandStr=="rss":
                    pypoca.rsstest()
                    continue

            print()                    
            print("  FEHLER: ")
            print("    Entweder konnte die Datenbank nicht geöffnet werden,")
            print("     oder der eingegebene Befehl ist falsch geschrieben!")
            print()
            print("  Datenbankstatus: "+str(dbstatus))

    else:
        if pypoca.loadConfig() < 2:
            pypoca.showList()


if __name__ == '__main__':
    starten()
