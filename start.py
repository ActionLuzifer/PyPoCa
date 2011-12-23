#!/usr/bin/python3

'''
Created on 2011-09-24

@author: actionluzifer
'''

import sys
sys.path.append("source");
import PyPoCa


if __name__ == '__main__':
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
                pypoca.addPodcast(sys.argv[i+1])
            elif commandStr=="addf":
                pypoca.loadConfig()
                pypoca.addPodcastByFile(sys.argv[i+1])
            elif commandStr=="removeI":
                pypoca.loadConfig()
                pypoca.removePodcastByID(sys.argv[i+1])
            elif commandStr=="removeN":
                pypoca.loadConfig()
                pypoca.removePodcastByName(sys.argv[i+1])
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
    else:
        pypoca.loadConfig()
        pypoca.list()
#        pypoca.loadConfig()
#        pypoca.update()
#        pypoca.download()
