'''
Created on Mar 5, 2015

@author: pilgrim
'''

import sys

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from PyQt5.QtWidgets import (QWidget, QApplication, QMenu, QAction, QHBoxLayout)
from stanguinic.ModelWidgets import QMoveableIconLabel, ConnectorNode, ParameterWidget, ConnectorLine
from stanguinic.widgets.DataWidget import DataWidget
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
            if hasattr(event, 'droppedOn') and self.dragline[0].validDrop(event.droppedOn):                
                event.droppedOn.connections = event.droppedOn.connections +1
                self.dragline[0].connections = self.dragline[0].connections + 1
                self.connections.append(ConnectorLine(self.dragline[0], event.droppedOn))
            self.dragline = None
        self.update()
    
    # Override - item dragged onto canvas
    def dragEnterEvent(self, event):
        event.accept()
        
    # Override - item dragged over canvas
    def dragMoveEvent(self, event):
        if isinstance(event.source(), QMoveableIconLabel):
            event.source().processMove(event)
        elif isinstance(event.source(), ConnectorNode):
            if event.source().full():
                # if it is full find the connector and disconnect this point
                event.source().connections = event.source().connections - 1
                relcon = next(e for e in self.connections if e.endsWith(event.source()))
                #self.dragline = (self.mapFromGlobal(relcon.start.globalPosition()), event.pos())
                self.dragline = (relcon.start, event.pos())
                self.connections.remove(relcon)
            else:
                self.dragline = (self.dragline[0] if self.dragline else
                                 event.source(), event.pos())
        self.update()
                
    # Handles right-clicks on canvas
    def contextMenuEvent(self, event):
        action = self.rcmenu.exec_(self.mapToGlobal(event.pos()))
        if action == self.actions['addData']:
            self.addData(event.pos())
        elif action == self.actions['addParameter']:
            self.addParameter(event.pos())
    
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
        
    def drawBezConnection(self, connection, painter):
        startp = self.mapFromGlobal(connection.start.globalPosition())
        endp = self.mapFromGlobal(connection.end.globalPosition())
        self.drawBez(startp, endp, painter)
    
    def drawBez(self, sp, ep, painter):
        midx = (sp.x() + ep.x()) / 2
        painter.moveTo(sp)
        p1 = QPoint(midx, sp.y())
        p2 = QPoint(midx, ep.y())
        painter.cubicTo(p1, p2, ep)
        
    def paintEvent(self, event):
        qp = QPainter()
        qpp = QPainterPath()
        qp.begin(self)
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        if self.dragline != None:
            self.drawBez(self.mapFromGlobal(self.dragline[0].globalPosition()), self.dragline[1], qpp)
        for c in self.connections:
            self.drawBezConnection(c, qpp)
        qp.drawPath(qpp)
        qp.end()
    
    # Opens the add data menu and adds the new parameter    
    def addData(self, pos):
        dataObject = DataWidget.createDialog()
        if not dataObject:
            return
        
        ic = DataWidget(self, dataObject)
        self.model.addData(ic.id, ic.model)
        self.dataWidgets.append(ic)
        ic.move(pos)
        ic.show()
    
    # Opens the add parameter menu and adds the new parameter
    def addParameter(self, pos):
        dataObject = ParameterWidget.createDialog()
        if not dataObject:
            return
        
        ic = ParameterWidget(self, dataObject)
        self.model.addParameter(ic.id, ic.model)
        self.dataWidgets.append(ic)
        ic.move(pos)
        ic.show()