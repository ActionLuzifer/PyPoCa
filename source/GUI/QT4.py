# coding=utf-8
'''
Created on 14.08.2013

@author: Duncan MC Leod
'''


from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
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
        if self.scrollWidget.verticalScrollBar().maximum() != self.scrollWidget.verticalScrollBar().minimum():
            self.scrollWidget.emit(QtCore.SIGNAL(self.scrollWidget.SIGNAL_onWidthChange), self.scrollWidget.getWidthForButtons())



    def _fcreateMenus(self):
        self.menuBar = QtGui.QMenuBar(self)
        self.menuPlugins = self.menuBar.addMenu("&Menü")
        self.testaction = QtGui.QAction("Zeige alle Podcasts", self)
        self.menuPlugins.addAction(self.testaction)
        self.connect(self.testaction, QtCore.SIGNAL("triggered()"), self.showPodcasts)
        self.menuBar.show()


    def priv_loadAllPodcast(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setText("Ich lade jetzt alle Podcasts")
        msgBox.exec()
        print("self.pypoca.downloadAll()")


    def priv_loadSelectedPodcast(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        for btn in self.btnHandler.buttonListSelected:
            msgBox.setText(str(btn.number)+btn.title)
            msgBox.exec()


    def priv_updateAllPodcasts(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setText("Ich update jetzt alle Podcasts")
        msgBox.exec()
        print("self.pypoca.updateAll()")
        

    def priv_updateSelectedPodcasts(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setText("Ich update jetzt diese Podcasts:")
        msgBox.exec()
        for btn in self.btnHandler.buttonListSelected:
            msgBox.setText(str(btn.number)+btn.title)
            msgBox.exec()


    def _createMainPage(self):
        abstandX = 5
        abstandY = 5
        btnLoadSelectedYdelta = self.menuBar.height()+abstandY
        
                
        btnUpdateAll = QPushButton("Update alle Podcasts", self)
        btnUpdateAll.move(abstandX, btnLoadSelectedYdelta)
        btnUpdateAll.show()
        self.connect(btnUpdateAll, QtCore.SIGNAL("clicked()"), self.priv_updateAllPodcasts)
        
        btnUpdateSelected      = QPushButton("Update ausgewählte Podcasts", self)
        btnUpdateSelected.move(btnUpdateAll.x()+btnUpdateAll.width()+abstandX, btnLoadSelectedYdelta)
        btnUpdateSelected.show()
        self.connect(btnUpdateSelected, QtCore.SIGNAL("clicked()"), self.priv_updateSelectedPodcasts)
        
        btnLoadAll = QPushButton("Lade alle Podcasts", self)
        btnLoadAll.move(btnUpdateSelected.x()+btnUpdateSelected.width()+abstandX, btnLoadSelectedYdelta)
        btnLoadAll.show()
        self.connect(btnLoadAll, QtCore.SIGNAL("clicked()"), self.priv_loadAllPodcast)
        
        btnLoadSelected = QPushButton("Lade ausgewählten Podcast", self)
        btnLoadSelected.move(btnLoadAll.x()+btnLoadAll.width()+abstandX, btnLoadSelectedYdelta)
        btnLoadSelected.show()
        self.connect(btnLoadSelected, QtCore.SIGNAL("clicked()"), self.priv_loadSelectedPodcast)
        
        self.scrollWidgetDelta = btnLoadSelectedYdelta + btnUpdateAll.height()+10
        self.scrollWidget = PyScrollWidget(self)
        self.scrollWidget.move(0, self.scrollWidgetDelta)
        self.scrollWidget.resize(self.width(), self.height()-self.scrollWidgetDelta)
        self.btnHandler = PyAbstractItemHandler(self.scrollWidget)
        self.scrollWidget.show()


    def resizeEvent(self, _resizeEvent):
        if self.scrollWidget:
            if self.height() > self.scrollWidgetDelta:
                self.scrollWidget.resize(self.width(), self.height()-self.scrollWidgetDelta)

