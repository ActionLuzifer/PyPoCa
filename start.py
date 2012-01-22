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
    if (len(sys.argv) > 1):
        i = 0
        while not i == len(sys.argv)-1:
            i+=1
            commandStr = sys.argv[i]
            print(len(sys.argv))
            print(commandStr)
            if commandStr=="update":
                pypoca.loadConfig()
                pypoca.update()
            elif commandStr=="download":
                pypoca.loadConfig()
                pypoca.download()
            elif commandStr=="add":
                pypoca.loadConfig()
                pypoca.addPodcastByURL(sys.argv[i+1])
                pypoca.saveConfig()
            elif commandStr=="addf":
                pypoca.loadConfig()
                pypoca.addPodcastByFile(sys.argv[i+1])
                pypoca.saveConfig()
            elif commandStr=="removeI":
                pypoca.loadConfig()
                pypoca.removePodcastByID(sys.argv[i+1])
                pypoca.saveConfig()
            elif commandStr=="removeN":
                pypoca.loadConfig()
                pypoca.removePodcastByName(sys.argv[i+1])
                pypoca.saveConfig()
            elif commandStr=="enableI":
                pypoca.loadConfig()
                pypoca.enablePodcastByID(sys.argv[i+1])
            elif commandStr=="enableN":
                pypoca.loadConfig()
                pypoca.disablePodcastByName(sys.argv[i+1])
            elif commandStr=="disableI":
                pypoca.loadConfig()
                pypoca.disablePodcastByID(sys.argv[i+1])
            elif commandStr=="disableN":
                pypoca.loadConfig()
                pypoca.enablePodcastByName(sys.argv[i+1])
            elif commandStr=="--version" or commandStr=="-v":
                pypoca.printVersion()
            elif commandStr=="--help" or commandStr=="-h":
                pypoca.printHelp()
            elif commandStr=="list":
                pypoca.loadConfig()
                pypoca.list()
            elif commandStr=="rss":
                pypoca.loadConfig()
                pypoca.rsstest()
    else:
        pypoca.loadConfig()
        pypoca.list()
#        pypoca.update()
#        pypoca.download()


if __name__ == '__main__':
    starten()
