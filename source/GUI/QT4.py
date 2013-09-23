# coding=utf-8
'''
Created on 14.08.2013

@author: Duncan MC Leod
'''


from PyQt4 import QtGui, QtCore
from PyQt4 import Qt
from source import PyPoCa
from source.GUI.PyItem import PyAbstractItemHandler, PyScrollWidget

class PyPoCaGUI_QT(QtGui.QWidget):
    
    def __init__(self, _pypoca, _width=800, _height=600, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        
                
        self.pypoca = _pypoca
        self.maxWidth  = 0
        self.maxHeight = 0
        self.move(120,30)
        
        self._fcreateMenus()
        self._createMainPage()

        self.resize(_width,_height)        
        self.show()


    def showPodcasts(self):
        podcasts = self.pypoca.getPodcasts()
        print("anzahl Podcasts:", len(podcasts))
        for podcast in podcasts:
            self.btnHandler.addButton(podcast.getID(), podcast.getName())


    def _fcreateMenus(self):
        self.menuBar = QtGui.QMenuBar(self)
        self.menuPlugins = self.menuBar.addMenu("&Menü")
        self.testaction = QtGui.QAction("Zeige alle Podcasts", self)
        self.menuPlugins.addAction(self.testaction)
        self.connect(self.testaction, Qt.SIGNAL("triggered()"), self.showPodcasts)
        self.menuBar.show()


    def priv_loadSelectedPodcast(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        for btn in self.btnHandler.buttonListSelected:
            msgBox.setText(btn.title)
            msgBox.exec()


    def _createMainPage(self):
        goButtonYdelta = self.menuBar.height()+5
        self.goButton = Qt.QPushButton("Lade ausgewählten Podcasts", self)
        self.goButton.move(0, goButtonYdelta)
        self.goButton.show()
        self.connect(self.goButton, Qt.SIGNAL("clicked()"), self.priv_loadSelectedPodcast)
        
        
        self.scrollWidgetDelta = goButtonYdelta + self.goButton.height()+10
        self.scrollWidget = PyScrollWidget(self)
        self.scrollWidget.move(0, self.scrollWidgetDelta)
        self.scrollWidget.resize(self.width(), self.height()-self.scrollWidgetDelta)
        self.btnHandler = PyAbstractItemHandler(self.scrollWidget)
        self.scrollWidget.show()


    def resizeEvent(self, _resizeEvent):
        if self.scrollWidget:
            if self.height() > self.scrollWidgetDelta:
                self.scrollWidget.resize(self.width(), self.height()-self.scrollWidgetDelta)

