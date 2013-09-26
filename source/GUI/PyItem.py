#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 17.08.2013

@author: Duncan MC Leod
'''

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QApplication, QFrame, QPalette, QScrollArea, QCursor, QColor
from PyQt4.QtCore import pyqtSignal, QObject, QPoint



class PyScrollWidget(QScrollArea):
    def __init__(self, _parent=None):
        QScrollArea.__init__(self, _parent)
    
        self.setMouseTracking(True)
        # ScrollBarAlwaysOff == 1
        # TODO: Finden wo "ScrollBarAlwaysOff" definiert ist und dann einsetzen statt der Zahl
        self.setHorizontalScrollBarPolicy(1)
        
        if _parent:
            self.setGeometry(_parent.geometry())
        else:
            self.setGeometry(1,1,1,1)

        self.btnWidget = QWidget(self)
        self.btnWidget.setMouseTracking(True)
        self.oldSizeX = 0
        self.oldSizeY = 0
        self.oldSizeWidth  = 1
        self.oldSizeHeight = 1 
        self.btnWidget.setGeometry(self.oldSizeX, self.oldSizeY, self.oldSizeWidth, self.oldSizeHeight)
        self.setWidget(self.btnWidget)
        
        self.scrollX = 0
        self.scrollY = 0
        
        self.setFrameStyle(1)
        
        # SIGNALS
        self.SIGNAL_onWidthChange = 'SIGNAL_widthchange(PyQt_PyObject)'
        self.SIGNAL_mousepress    = 'SIGNAL_mousepress(PyQt_PyObject)'
        self.SIGNAL_mousemove     = 'SIGNAL_mousemove(PyQt_PyObject)'
        self.SIGNAL_mouserelease  = 'SIGNAL_mouserelease(PyQt_PyObject)'
        

    def resizeEvent(self, _resizeEvent):
        newWidthScrollArea = self.size().width()
        if newWidthScrollArea != self.oldSizeWidth:
            if self.verticalScrollBar().isVisible():
                newWidthBtnWidget = self.width()-self.verticalScrollBar().width()
            else:
                newWidthBtnWidget = self.width()
            
            self.btnWidget.resize(newWidthBtnWidget, self.btnWidget.height())
            self.oldSizeWidth = self.btnWidget.size().width()
            
            self.emit(QtCore.SIGNAL(self.SIGNAL_onWidthChange), newWidthBtnWidget-3)
        pass
        
        return QScrollArea.resizeEvent(self, _resizeEvent)


    def onScroll(self):
        self.emit(QtCore.SIGNAL(self.SIGNAL_onScroll))


    def isButtonVisible(self, _button):
        if ( _button.y() > self.scrollY) and (_button.y() < (self.scrollY + self.height()) ):
            return True
        else:
            return False


    def mouseMoveEvent(self, _qmouseevent):
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousemove), _qmouseevent)
        return QWidget.mouseMoveEvent(self, _qmouseevent)


    def mousePressEvent(self, _event):
        self.emit(QtCore.SIGNAL(self.SIGNAL_mousepress), _event)
        return QWidget.mousePressEvent(self, _event)


    def mouseReleaseEvent(self, _event):
        self.emit(QtCore.SIGNAL(self.SIGNAL_mouserelease), _event)
        return QWidget.mouseReleaseEvent(self, _event)



class PyAbstractItemHandler(QObject):

    def __init__(self, _scrollWidget):
        QObject.__init__(self)
        
        # scrollwidget erhalten und verbinden
        self.scrollWidget = _scrollWidget
        self.btnWidget = self.scrollWidget.btnWidget
        
        
        self.SIGNAL_ZOOM          = 'SIGNAL_ZOOM(PyQt_PyObject)'
        
        ### CONNECTIONS ###
        # WidthChange        
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_onWidthChange), self.slotOnWidthChange)
        # MouseMove
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_mousemove), self.mouseMoveEvent)
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_mousepress), self.mousePressEvent)
        QObject.connect(self.scrollWidget, QtCore.SIGNAL(self.scrollWidget.SIGNAL_mouserelease), self.mouseReleaseEvent)
        
        self.buttonHeight = 20
        self.buttonGap = 10
        self.buttonList = []
        self.buttonListVisible = []
        self.buttonHovered = None
        self.buttonListSelected = []
        self.isMultiSelection = False
        self.buttonListIsEmpty = True
        self.isMousePressed = False
        self.oldMousePos = QPoint(0,0)
        self.mouseMoveDirection = None
        self.mouseVERTICAL = 1
        self.mouseHORIZONTAL = 2
        self.vertScrollbarPosOld = 0
        self.isMouseScroll = False
        self.btnMousePress = None
        self.btnZooming = None


    def addButton(self, _no, _title):
        x = 0
        if self.buttonListIsEmpty:
            y = (len(self.buttonList))*self.buttonHeight
            self.buttonListIsEmpty = False
        else:
            y = (len(self.buttonList))*(self.buttonHeight+self.buttonGap)

        item = PyItem(self.scrollWidget.btnWidget, self, _no, _title, x, y, self.scrollWidget.width()-20, self.buttonHeight)
        self.btnWidget.resize(self.btnWidget.width(), y+self.buttonHeight)
        item.oY = y 

        self.buttonList.append(item)
        item.setFrameStyle(1)
        item.show()


    def getMouseKoords(self):
        return self.scrollWidget.mapFromGlobal(QCursor.pos())


    def getBtnUnderMouse(self, _koord):
        '''Returns the Button which has this koordinates in its region.
        '''
        theBtn = None
        vertScrollBarVerschiebung = self.scrollWidget.verticalScrollBar().value()
        koordX = _koord.x()
        koordY = _koord.y()+vertScrollBarVerschiebung
        for btn in self.buttonList:
            if ( (btn.x() < koordX)
                 and (btn.y() < koordY)
                 and (btn.x() + btn.width() > koordX)
                 and (btn.y() + btn.height() > koordY)):
                theBtn = btn
                break
        return theBtn


    def checkForHovering(self, mousePos):
        # moeglicherweise ist ein Button unter der Maus
        btn = self.getBtnUnderMouse(mousePos)
        if btn:            
            # wenn über nem Button -> hovern
            self.onMouseHover(btn)
        else:
            if self.buttonHovered:
                self.buttonHovered.isHovered = False
                self.buttonHovered.decorate()
                self.buttonHovered = None


    def onMouseHover(self, _button):
        if self.buttonHovered:
            self.buttonHovered.isHovered = False
            self.buttonHovered.decorate()
        _button.isHovered = True
        _button.decorate()
        self.buttonHovered = _button


    def onScroll(self):
        for button in self.buttonListVisible:
            button.hide()
        
        for button in self.buttonList:
            if self.isButtonVisible(button):
                self.buttonListVisible.append(button)

    def isButtonVisible(self, _button):
        if ( _button.y() > self.scrollWidget.scrollY) and (_button.y() < (self.scrollWidget.scrollY + self.scrollWidget.height()) ):
            return True
        else:
            return False
        
    def mouseMoveEvent(self, _qmouseevent):
        mousePos = self.getMouseKoords()
        if self.isMousePressed:
            # ich werde entweder scrollen oder 'in den Button zoomen' wollen
            vertDelta = mousePos.y()-self.oldMousePos.y()
            print("abs(vertDelta):",abs(vertDelta))
            horzDelta = mousePos.x()-self.oldMousePos.x()
            if ((abs(vertDelta) > 10) 
                and ((self.mouseMoveDirection == None) or (self.mouseMoveDirection == self.mouseVERTICAL))):
                
                self.mouseMoveDirection = self.mouseVERTICAL
                unterschied = mousePos.y() - self.oldMousePos.y()
                
                scrollbarPosNew = self.vertScrollbarPosOld-unterschied
                self.scrollWidget.verticalScrollBar().setValue(scrollbarPosNew)
                self.isMouseScroll = True
            elif (abs(horzDelta) > 10) and ( (self.mouseMoveDirection == None) or (self.mouseMoveDirection == self.mouseHORIZONTAL) ):
                self.mouseMoveDirection = self.mouseHORIZONTAL
                btn = self.getBtnUnderMouse(mousePos)
                if btn:
                    self.btnZooming = btn
                    btn.isZooming = True
                    btn.decorate()
                
                # 'Zoom' in den Button
        else:
            self.checkForHovering(mousePos)


    def mousePressEvent(self, _event):
        
        mouseKoords = self.getMouseKoords()
        self.btnMousePress = self.getBtnUnderMouse(mouseKoords)
        
        if self.btnMousePress:
            self.btnMousePress.isMousePress = True
            self.btnMousePress.isSelectedForScroll = True
            self.btnMousePress.decorate()

        self.btnZooming = None
        self.isMousePressed = True
        self.oldMousePos = mouseKoords
        self.vertScrollbarPosOld = self.scrollWidget.verticalScrollBar().value()


    def mouseReleaseEvent(self, _event):
        mouseKoords = self.getMouseKoords()
        self.oldMousePos = mouseKoords
        self.isMousePressed = False
        self.isMouseScroll = False
        
        # dekorieren & aufräumen
        # wenn beim loslassen der Cursor über dem Button liegt und nicht gescrollt wurde, dann ist er Selected
        btn = self.getBtnUnderMouse(mouseKoords)
        if btn:
            if btn == self.btnMousePress:
                if not self.isMouseScroll and self.btnZooming == None:
                    # wurde nicht gescrollt, sondern der Button wurde ausgewählt
                    if not self.isMultiSelection:
                        # alte Buttons deselektieren
                        for btnSelected in self.buttonListSelected:
                            btnSelected.isSelectedForScroll = False
                            btnSelected.isSelected = False
                            btnSelected.decorate()
                        self.buttonListSelected = []
                    btn.isSelected = True
                    self.buttonListSelected.append(btn)
                elif self.btnZooming:
                    self.emit(QtCore.SIGNAL(self.SIGNAL_ZOOM), self.btnZooming)
                    self.btnZooming.isZooming = False
                    self.btnZooming.decorate()
                    self.btnZooming = None
                # der beim MousePress ausgewählte Button wird deselektiert
                if self.btnMousePress:
                    self.btnMousePress.isSelectedForScroll = False
                    self.btnMousePress.isMousePress = False
                    self.btnMousePress.decorate()
            else:
                # der beim MousePress ausgewählte Button wird deselektiert
                if self.btnMousePress:
                    self.btnMousePress.isSelectedForScroll = False
                    self.btnMousePress.isMousePress = False
                    self.btnMousePress.decorate()
            
            # aktuellen Button deselektieren
            btn.isSelectedForScroll = False
            btn.isMousePress = False
            btn.decorate()

        else:
            # der beim MousePress ausgewählte Button wird deselektiert
            if self.btnMousePress:
                self.btnMousePress.isSelectedForScroll = False
                self.btnMousePress.isMousePress = False
                self.btnMousePress.decorate()
                
        self.isMousePressed = False
        self.mouseMoveDirection = None
        self.isMouseScroll = False
        self.btnMousePress = None
        self.checkForHovering(mouseKoords)


    def slotOnWidthChange(self, _width):
        for btn in self.buttonList:
            btn.resize(_width, btn.size().height())



class PyAbstractItem(QFrame):
    
    def __init__(self, _parent, _itemHandler, _x=0, _y=0, _width=100, _height=20):
        QFrame.__init__(self, _parent)
        self.itemHandler = _itemHandler
        self.isMousePress = False
        self.isSelected = False
        self.isHovered = False
        self.isZooming = False
        self.isSelectedForScroll = False
        
        self.decorateNormal()
        self.move(_x,_y)
        self.resize(_width,_height)
        self.show()


    def decorateNormal(self):
        # Die normalen Anzeigeeinstellungen einstellen
        self.setStyleSheet("background-color: white;");


    def decorateHover(self):
        # Anzeigeeinstellungen wenn Maus rüberfährt
        self.setStyleSheet("background-color: blue;");


    def decorateZooming(self):
        self.setStyleSheet("background-color: purple;")


    def decorate(self):
        if self.isZooming:
            self.decorateZooming()
        elif self.isMousePress:
            # mousePress = selected & hovered gleichzeitig
            if self.isSelected:
                # (halb)Selected, Hovered und selected
                self.decorateHalfselectedAndHoveredAndSelected()
                pass
            else:
                # (halb)Selected und Hovered
                self.decorateHalfselectedAndHovered()
                pass
        elif self.isSelected:
            if self.isHovered:
                # selected und hovered
                self.decorateSelectedAndHovered()
                pass
            else:
                # nur seclected
                self.decorateSelected()
        elif self.isHovered:
            # nur hover
            self.decorateHover()
        else:
            self.decorateNormal()


    def decorateHalfselectedAndHoveredAndSelected(self):
        self.setStyleSheet("background-color: green;")


    def decorateHalfselectedAndHovered(self):
        self.setStyleSheet("background-color: yellow;")

    def decorateSelectedAndHovered(self):
        self.setStyleSheet("background-color: red;")


    def decorateSelected(self):
        # Anzeigeeinstellungen wenn Objekt z.b. per Mausklick oder Tastaturcursor ausgewählt wurde
        self.setStyleSheet("background-color: orange;")
        pass



class PyItem(PyAbstractItem):
    
    def __init__(self, _parent, _itemHandler, _number, _title, _x, _y, _width, _height):
        PyAbstractItem.__init__(self, _parent, _itemHandler, _x, _y, _width, _height)
        #PyAbstractItem.setMouseTracking(self, True)
        self.setMouseTracking(True)
        self.number = _number
        self.title = _title
        self.titleLabel = QtGui.QLabel(self)
        self.titleLabel.setText(self.title)
        self.titleLabel.move(3,3)
        self.titleLabel.show()
