"""
Created on 05.11.2011

@author: DuncanMCLeod
"""

import source.Downloader.BasisDownloader as BasisDownloader
import urllib.request
from urllib.error import HTTPError, URLError
import source.SQLs as SQLs
import sys
from io import BufferedWriter

class Intern(BasisDownloader.Downloader):
    """Downloadklasse die mithilfe von den Pythonklassen die Dateien herunterlaedt"""
   
    def download(self, _id, castFileName, url, status):
        castFile = None
        isError = False
        fileOptions = ''
        # Datei NEU oder beim letzten Versuch nen Fehler jehabt?
        if (status==SQLs.episodestatus["new"]) or (status==SQLs.episodestatus["error"]):
            fileOptions = 'wb' 
        # Datei Unvollstaendig?
        elif status==SQLs.episodestatus["incomplete"]:
            fileOptions = 'ab'

        try:
            castFile = open(castFileName, fileOptions)
            downloaddingens = urllib.request.urlopen(url)
            statuscode = downloaddingens.getcode()
            castFile.write(downloaddingens.read())
        except HTTPError as e:
            print("HTTP Error at URL: ", url)
            print("HTTP ErrorCode:    ", e.code)
            print("HTTP ErrorReason:  ", e.reason)
            statuscode = e.code
            isError = True
        except URLError as e:
            print("URL Error at URL:  ", url)
            print("URL ErrorReason :  ", e.reason)
            statuscode = e.reason
            isError = True
        except:
            exctype, value = sys.exc_info()[:2]
            print("ERROR"+repr(exctype))
            print("   ->"+repr(value))
            print("   ->url:          "+url)
            try:
                print("   ->castFileName: "+castFileName)
            except:
                pass
            isError = True
            statuscode = "unknown"
        finally:
            if type(castFile) is BufferedWriter:
                castFile.close()
        return isError, statuscode
