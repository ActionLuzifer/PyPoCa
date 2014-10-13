"""
Created on 27.09.2011

@author: DuncanMCLeod
"""

sqlCREATEpodcasts = "CREATE TABLE podcasts (castid INTEGER CONSTRAINT primkey PRIMARY KEY, castname TEXT NOT NULL, casturl TEXT NOT NULL, status INTEGER NOT NULL);"
sqlINSERTpodcasts = "INSERT INTO podcasts VALUES (?, ?, ?, ?);"
sqlUPDATEpodcasts_name    = "UPDATE podcasts SET castname=? WHERE castid=?;"
sqlUPDATEpodcasts_url     = "UPDATE podcasts SET casturl=? WHERE castid=?;"
sqlUPDATEpodcasts_status  = "UPDATE podcasts SET status=? WHERE castid=?;"
sqlDELETEpodcasts = "DELETE FROM podcasts WHERE castid=?;"
sqlSELECTpodcasts = "SELECT * FROM podcasts WHERE castid=?"

#hpodder:
#CREATE TABLE "episodes" (castid INTEGER NOT NULL,episodeid INTEGER NOT NULL,title TEXT NOT NULL,epurl TEXT NOT NULL,enctype TEXT NOT NULL,status TEXT NOT NULL,eplength INTEGER NOT NULL DEFAULT 0,epfirstattempt INTEGER,eplastattempt INTEGER,epfailedattempts INTEGER NOT NULL DEFAULT 0,epguid TEXT,UNIQUE(castid, epurl),UNIQUE(castid, episodeid),UNIQUE(castid, epguid))
sqlCREATEepisodes = "CREATE TABLE episodes (castid INTEGER NOT NULL, episodeid INTEGER NOT NULL, episodeURL TEXT NOT NULL, episodeNAME TEXT NOT NULL, episodeGUID TEXT NOT NULL, status INT NOT NULL, UNIQUE(castid, episodeid));"
sqlINSERTepisodes = "INSERT INTO episodes VALUES (?, ?, ?, ?, ?, ?);"
sqlUPDATEepisodes_episodeURL  = "UPDATE episodes SET episodeURL=? WHERE castid=? AND episodeid=?;"
sqlUPDATEepisodes_episodeNAME = "UPDATE episodes SET episodeNAME=? WHERE castid=? AND episodeid=?;"
sqlUPDATEepisodes_episodeGUID  = "UPDATE episodes SET episodeGUID=? WHERE castid=? AND episodeid=?;"
sqlUPDATEepisodes_status      = "UPDATE episodes SET status=? WHERE castid=? AND episodeid=?;"
sqlDELETEepisodes = "DELETE FROM episodes WHERE castid=? AND episodesid=?;"
sqlDELETEepisodesByCast = "DELETE FROM episodes WHERE castid=?;"
sqlSELECTepisodesByCast = "SELECT * FROM episodes WHERE castid=? ORDER BY episodeid;"

episodestatus = {"new":1, "downloaded":2, "error":3, "incomplete":4, "404":404}


sqlCREATEconfig = "CREATE TABLE config (confid INTEGER CONSTRAINT primkey PRIMARY KEY, confname TEXT NOT NULL, confdata TEXT NOT NULL);"
sqlINSERTconfig = "INSERT INTO config VALUES (?, ?, ?);"
sqlINSERTconfig_lastCastID    = sqlINSERTconfig.format(0, 'lastCastID', 0)
sqlINSERTconfig_numberOfCasts = sqlINSERTconfig.format(1, 'numberOfCasts', 0)
sqlINSERTconfig_lastused      = sqlINSERTconfig.format(2, 'lastused', 0)
sqlUPDATEconfig_lastCastID    = "UPDATE config SET confdata=? WHERE confid=0;"
sqlUPDATEconfig_numberOfCasts = "UPDATE config SET confdata=? WHERE confid=1;"
sqlUPDATEconfig_lastused      = "UPDATE config SET confdata=? WHERE confid=2;"


sqlgetAllTables = "SELECT name, sql FROM sqlite_master WHERE type='table' ;"
sqlGETALLpodcasts = "SELECT * from podcasts ORDER BY castid"
sqlGETALLconfig = "SELECT * from config"

sqlCREATEcastsAndEpisodes = "CREATE TABLE podcastsAndEpisodes (castID INTEGER NOT NULL, highestEpisodeID INTEGER NOT NULL, UNIQUE(castid, highestEpisodeID));"
sqlINSERTcastsAndEpisodes = "INSERT INTO podcastsAndEpisodes VALUES (?, ?);"
sqlUPDATEcastsAndEpisodes = "UPDATE podcastsAndEpisodes SET highestEpisodeID=? WHERE castID=?;"
sqlDELETEcastsAndEpisodes = "DELETE FROM podcastsAndEpisodes WHERE castID=?;"
sqlSELECTcastsAndEpisodes = "SELECT highestEpisodeID FROM podcastsAndEpisodes WHERE castID=?"
