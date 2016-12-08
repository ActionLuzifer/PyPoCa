#!/usr/bin/python3
# coding=utf-8
"""
Created on 2011-09-24

@author: actionluzifer
"""

import sys
import source.PyPoCa as PyPoCa
from source.PyPoCaDB import DB_NOERROR, DB_LOCKED, DB_UNKNOWN
import source.GUI.Console as Console
import argparse



def starten():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qt",                     help="Start with a QT-GUI",                           action="store_true")
    parser.add_argument("--id",                     help="If you want to change something (URL, NAME, ...) "
                       +"you has to provide the ID for that",                                             action="store_true")
    parser.add_argument("--download",               help="download every episode",                        action="store_true")
    parser.add_argument("--downloadID",             help="download only the episodes of this podcast"                        )
    parser.add_argument("--update",                 help="update all podcasts",                           action="store_true")
    parser.add_argument("--updateID",               help="update only the podcast with this ID"                              )
    parser.add_argument("--add",                    help="add an http(s)-podcast"                                            )
    parser.add_argument("--addf",                   help="add a file-based podcast"                                          )
    parser.add_argument("--remove",                 help="remove a podcast"                                                  )
    parser.add_argument("--enable",                 help="enable a podcast"                                                  )
    parser.add_argument("--disable",                help="disable a podcast"                                                 )
    parser.add_argument("--rename",                 help="rename a podcast (provide an ID)"                                  )
    parser.add_argument("--changeURL",              help="change the URL an a podcast (provide an ID)"                       )
    parser.add_argument("--showNewEpisodes",        help="show all new episodes",                         action="store_true")
    parser.add_argument("--showIncompleteEpisodes", help="show all incomplete episodes",                  action="store_true")
    parser.add_argument("--version",                help="show the version of PyPoCa",                    action="store_true")
    parser.add_argument("--helpme",                 help="show the internal help (maybe not up to date)", action="store_true")
    parser.add_argument("--list",                   help="list all podcasts",                             action="store_true")
    parser.add_argument("--listEpisodes",           help="list all episodes of every podcast",            action="store_true")
    parser.add_argument("--rss",                    help="test....some...rss..file",                      action="store_true")


    args = parser.parse_args()

    pypoca = PyPoCa.PyPoCa()
    consoleGUI = Console.Console()
    pypoca.registerGUI(consoleGUI)

    if len(args.__dict__)==0:
        dbstatus = pypoca.loadConfig()
        if dbstatus == DB_NOERROR:
            if args.qt is not None:
                from source.GUI import QT4
                from PyQt4 import QtGui
                qapp = QtGui.QApplication(sys.argv)
                dingdong = QT4.PyPoCaGUI_QT(pypoca)  # @unusedVariable
                sys.exit(qapp.exec_())
            else:
                if args.update is not None:
                    pypoca.updateAll()

                elif args.updateID:
                    pypoca.updateID(args.updateID)

                elif args.download is not None:
                    downloadedEpisodes = pypoca.downloadAll()
                    pypoca.writePlaylist(downloadedEpisodes, pypoca.getPlaylistFilename())

                elif args.downloadID is not None:
                    downloadedEpisodes = pypoca.downloadID(args.downloadID)
                    pypoca.writePlaylist(downloadedEpisodes, pypoca.getPlaylistFilename())

                elif args.add is not None:
                    pypoca.addPodcastByURL(args.add)
                    pypoca.saveConfig()

                elif args.addf is not None:
                    pypoca.addPodcastByFile(args.addf)
                    pypoca.saveConfig()

                elif args.remove is not None:
                    pypoca.removePodcastByID(args.remove)
                    pypoca.saveConfig()

                elif args.enable is not None:
                    pypoca.enablePodcastByID(args.enable)

                elif args.disable is not None:
                    pypoca.disablePodcastByID(args.disable)

                elif args.showNewEpisodes is not None:
                    pypoca.showNewEpisodes()

                elif args.showIncompleteEpisodes is not None:
                    pypoca.showIncompleteEpisodes()

                if args.rename or args.changeURL or args.updateID:
                    if args.id is None: print("ERROR: '--id' is missing")
                    elif args.rename is not None:
                        pypoca.renamePodcast(args.id, args.rename)

                    elif args.changeURL is not None:
                        pypoca.changeURLofPodcast(args.id, args.changeURL)

                    elif args.updateID is not None:
                        pypoca.updateID(args.updateID)

        elif dbstatus == DB_LOCKED:
            if args.version:
                pypoca.printVersion()
            elif args.helpme:
                pypoca.printHelp()
            elif args.list:
                pypoca.showList()
            elif args.listEpisodes:
                pypoca.showListEpisodes()
            elif args.rss:
                pypoca.rsstest()
        elif dbstatus == DB_UNKNOWN:
            print()
            print("Oh, ein bekannter unbekannter DB-Fehler trat auf")
            print("  FEHLER: ")
            print("    Entweder konnte die Datenbank nicht geöffnet werden,")
            print("     oder der eingegebene Befehl ist falsch geschrieben!")
            print()
            print("  Datenbankstatus: "+str(dbstatus))
        else:
            print("Upsi! Something terrible went wrong!")
    else:
        if pypoca.loadConfig() < 2:
            pypoca.showList()



if __name__ == '__main__':
    starten()
