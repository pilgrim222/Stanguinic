'''
Created on Mar 5, 2015

@author: pilgrim
'''

import sys

from PyQt5.QtWidgets import (QWidget, QApplication, QMenu, QAction, QHBoxLayout)
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

from stanguinic.ModelWidgets import DataWidget, QMoveableIconLabel, ConnectorNode
from stanguinic.StanModel import StanModel, SData

class StanCanvas(QWidget):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        super().__init__()
        
        #self.model = StanModel()
        self.actions = {}
        self.dataWidgets = []
        self.setAcceptDrops(True)
        self.createTestUI()
        self.createRightClickMenu()
        self.model = StanModel()
        self.connections = []
        self.dragline = None
        
    def createTestUI(self):
        self.resize(800,600)
        self.show()

    # Override - item dropped on canvas
    def dropEvent(self, event):
        if isinstance(event.source(), QMoveableIconLabel):            
            event.source().processMove(event)
        elif isinstance(event.source(), ConnectorNode):
            self.dragline = None
            if hasattr(event, 'droppedOn'):
                self.connections.append((event.source(), event.droppedOn))
        self.update()
    
    # Override - item dragged onto canvas
    def dragEnterEvent(self, event):
        event.accept()
        
    # Override - item dragged over canvas
    def dragMoveEvent(self, event):
        if isinstance(event.source(), QMoveableIconLabel):
            event.source().processMove(event)
        elif isinstance(event.source(), ConnectorNode):
            self.dragline = (self.mapFromGlobal(event.source().globalPosition()), event.pos())
        self.update()
                
    # Handles right-clicks on canvas
    def contextMenuEvent(self, event):
        action = self.rcmenu.exec_(self.mapToGlobal(event.pos()))
        if action == self.actions['addData']:
            self.addData(event.pos())
    
    def createRightClickMenu(self):
        self.rcmenu = QMenu(self)
        
        # Add data action
        addDataAction = QAction("Add data", self)
        self.actions['addData'] = addDataAction
        self.rcmenu.addAction(addDataAction)
        
        # Add parameter action
        addParamAction = QAction("Add parameter", self)
        self.actions['addParameter'] = addParamAction
        self.rcmenu.addAction(addParamAction)
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        if self.dragline != None:
            qp.drawLine(self.dragline[0], self.dragline[1])
        for (p1, p2) in self.connections:
            qp.drawLine(self.mapFromGlobal(p1.globalPosition()), self.mapFromGlobal(p2.globalPosition())) 
        qp.end()
        
    def addData(self, pos):
        dataObject = DataWidget.createDialog()
        if not dataObject:
            return
        
        ic = DataWidget(self, dataObject)
        self.model.addData(ic.id, ic.model)
        self.dataWidgets.append(ic)
        ic.move(pos)
        ic.show()