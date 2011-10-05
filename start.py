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
    pypoca.loadConfig()
    #pypoca.addPodcastByFile()
    pypoca.update()