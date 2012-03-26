'''
Created on 27.09.2011

@author: DuncanMCLeod
'''

sqlCREATEpodcasts = "CREATE TABLE podcasts (castid CONSTRAINT primkey PRIMARY KEY, castname, casturl, status);"
sqlINSERTpodcasts = "INSERT INTO podcasts VALUES ({0}, '{1}', '{2}', '{3}');"
sqlUPDATEpodcasts_name    = "UPDATE podcasts SET castname='{0}' WHERE castid={1};"
sqlUPDATEpodcasts_url     = "UPDATE podcasts SET casturl='{0}' WHERE castid={1};"
sqlUPDATEpodcasts_status  = "UPDATE podcasts SET status='{0}' WHERE castid={1};"
sqlDELETEpodcasts = "DELETE FROM podcasts WHERE castid={0};"
sqlSELECTpodcasts = "SELECT * FROM podcasts WHERE castid={0}"

#hpodder:
#CREATE TABLE "episodes" (castid INTEGER NOT NULL,episodeid INTEGER NOT NULL,title TEXT NOT NULL,epurl TEXT NOT NULL,enctype TEXT NOT NULL,status TEXT NOT NULL,eplength INTEGER NOT NULL DEFAULT 0,epfirstattempt INTEGER,eplastattempt INTEGER,epfailedattempts INTEGER NOT NULL DEFAULT 0,epguid TEXT,UNIQUE(castid, epurl),UNIQUE(castid, episodeid),UNIQUE(castid, epguid))
sqlCREATEepisodes = "CREATE TABLE episodes (castid INTEGER NOT NULL, episodeid INTEGER NOT NULL, episodeURL TEXT NOT NULL, episodeNAME TEXT NOT NULL, episodeGUID TEXT NOT NULL, status INT NOT NULL, UNIQUE(castid, episodeid), UNIQUE(castid, episodeURL));"
sqlINSERTepisodes = "INSERT INTO episodes VALUES ({0}, {1}, '{2}', '{3}', '{4}', {5});"
sqlUPDATEepisodes_episodeURL  = "UPDATE episodes SET episodeURL='{0}' WHERE castid={1} AND episodeid={2};"
sqlUPDATEepisodes_episodeNAME = "UPDATE episodes SET episodeNAME='{0}' WHERE castid={1} AND episodeid={2};"
sqlUPDATEepisodes_episodeGUID  = "UPDATE episodes SET episodeGUID='{0}' WHERE castid={1} AND episodeid={2};"
sqlUPDATEepisodes_status      = "UPDATE episodes SET status={0} WHERE castid={1} AND episodeid={2};"
sqlDELETEepisodes = "DELETE episodes WHERE castid={0} AND episodesid={1};"
sqlDELETEepisodesByCast = "DELETE episodes WHERE castid={0};"
sqlSELECTepisodesByCast = "SELECT * FROM episodes WHERE castid={0};"

episodestatus = {"new":1, "downloaded":2, "error":3, "incomplete":4}


sqlCREATEconfig = "CREATE TABLE config (confid CONSTRAINT primkey PRIMARY KEY, confname, confdata);"
sqlINSERTconfig = "INSERT INTO config VALUES ({0}, '{1}', '{2}');"
sqlINSERTconfig_lastCastID    = sqlINSERTconfig.format(0, 'lastCastID', 0)
sqlINSERTconfig_numberOfCasts = sqlINSERTconfig.format(1, 'numberOfCasts', 0)
sqlUPDATEconfig_lastCastID    = "UPDATE config SET confdata={0} WHERE confid=0;"
sqlUPDATEconfig_numberOfCasts = "UPDATE config SET confdata={0} WHERE confid=1;"


sqlgetAllTables = "SELECT name, sql FROM sqlite_master WHERE type='table' ;"
sqlGETALLpodcasts = "SELECT * from podcasts ORDER BY castid"
sqlGETALLconfig = "SELECT * from config"

sqlCREATEcastsAndEpisodes = "CREATE TABLE podcastsAndEpisodes (castID INTEGER NOT NULL, highestEpisodeID INTEGER NOT NULL, UNIQUE(castid, highestEpisodeID));"
sqlINSERTcastsAndEpisodes = "INSERT INTO podcastsAndEpisodes VALUES ({0}, {1});"
sqlUPDATEcastsAndEpisodes = "UPDATE podcastsAndEpisodes SET highestEpisodeID={1} WHERE castID={0};"
sqlDELETEcastsAndEpisodes = "DELETE podcastsAndEpisodes WHERE castid={0}"
sqlSELECTcastsAndEpisodes = "SELECT highestEpisodeID FROM podcastsAndEpisodes WHERE castID='{0}'"
