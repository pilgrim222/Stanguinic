'''
Created on Mar 11, 2015

@author: pilgrim
'''

import stanguinic.StanModel as StanModel

from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QGridLayout, QVBoxLayout, QFrame, QLayout, QSizePolicy
from PyQt5.QtCore import Qt, QMimeData, QSize, QEvent, QPoint
from PyQt5.QtGui import QDrag, QIcon
from stanguinic.StanDialog import SDataDialog
from stanguinic.StanModel import SData, SParameter
from PyQt5.Qt import QPixmap

class QMoveableIconLabel(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.indegree = 0
        self.outdegree = 0
        self.inConnectors = []
        self.outConnectors = []
        
    '''
    General class which functions as an icon + text with the ability
    to drag & drop it around its parent widget.
    The parent widget should call the processMove function on drop event.
    
    '''
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            drag.setMimeData(QMimeData())
            drag.setHotSpot(event.pos() - self.rect().topLeft())            
            drag.exec_(Qt.MoveAction)
    
    def mousePressEvent(self, event):
        self._moveDelta = event.pos()
    
    def processMove(self, dropEvent):
        self.move(dropEvent.pos() - self._moveDelta)
        
    # By default forwards drops to be handeled at the widget's parend
    def dropEvent(self, event):
        return self.parentWidget().dropEvent(event)
    
    # Creates the default visual representation (icon with text underneath)
    # Needs the initIcon function to be implemented and return a QPixmap object
    # containing the icon.    
    def createVisual(self, parameters):
        name = parameters['name']
        self.indegree = parameters['indegree']
        self.outdegree = parameters['outdegree']
        self.setLayout(QGridLayout())

        self.createIcon()
        self.createText(name)
        self.createInOutNodes()
        
        self.layout().addLayout(self._left,0,0)
        self.layout().addWidget(self._icon,0,1)
        self.layout().addLayout(self._right,0,2)
        
        self.layout().addWidget(self._text, 1, 1)
        
    def createIcon(self):
        self._icon = QLabel()
        self._icon.setPixmap(self.initIcon())
        
    def createText(self, name):
        self._text = QLabel(name)
        self._text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
    def createInOutNodes(self):
        self._left = ConnectorsLayout()
        self.inConnectors = self._left.initConnectors(self, self.indegree)
        self._right = ConnectorsLayout()
        self.outConnectors = self._right.initConnectors(self, self.outdegree) 
    
    def addInConnector(self):
        self.inConnectors.append(self._left.addConnector(self))
        self.indegree = self.indegree + 1
        
    def addOutConnector(self):
        self.outConnectors.append(self._right.addConnector(self))
        self.outdegree = self.outdegree + 1
    
    def updateVisual(self, newParams):
        self._text.setText(newParams['name'])
        
        if newParams['indegree'] != self.indegree:
            while self.indegree < newParams['indegree']:
                self.addInConnector()
                
            while self.indegree > newParams['indegree']:
                self.indegree = self.indegree - 1
                self._left.removeConnector(self.inConnectors[-1])
                del self.inConnectors[-1]
            
        if newParams['outdegree'] != self.outdegree:
            while self.outdegree < newParams['outdegree']:
               self.addOutConnector()
               
            while self.outdegree > newParams['outdegree']:
                self.outdegree = self.outdegree - 1
                self._right.removeConnector(self.outConnectors[-1])
                del self.outConnectors[-1]
                
    def event(self, e):
        if e.type() == QEvent.LayoutRequest:
            self.adjustSize()
            
        return super().event(e)

class DataWidget(QMoveableIconLabel):
    
    def __init__(self, parent, parameters):
        super().__init__(parent)
        self.id = parameters['name']
        self.createVisual(parameters)
        self.model = SData.fromDictionary(parameters)
        
    def updateParams(self, newParams):
        self.model.update(newParams)
    
    def mouseDoubleClickEvent(self, event):
        newparams = self.editDialog()
        if not newparams:
            return
        self.updateVisual(newparams)
        self.model.update(newparams)
    
    # Prompt user for new data item specification (static)
    @staticmethod
    def createDialog():
        dwdiag = SDataDialog()
        diagres = dwdiag.exec_()
        if not diagres: 
            return None
        return dwdiag.getInput()    
    
    def editDialog(self):
        params = self.model.getParams()
        editDiag = SDataDialog(params)
        val = editDiag.exec_()
        if not val: 
            return None
        return editDiag.getInput()
    
    def initIcon(self):
        return QPixmap("images/dataIcon.png").scaledToHeight(50)
    

class ParameterWidget(QMoveableIconLabel):
    def __init__(self, parent, parameters):
        super().__init__(parent)
        self.id = parameters['name']
        self.createVisual(parameters)
        self.model = SParameter.fromDictionary(parameters)
    
    def updateParams(self, newParams):
        self.model.update(newParams)
    
    def mouseDoubleClickEvent(self, event):
        newparams = self.editDialog()
        if not newparams:
            return
        self.updateVisual(newparams)
        self.model.update(newparams)
    
    # Prompt user for new data item specification (static)
    @staticmethod
    def createDialog():
        dwdiag = SDataDialog()
        diagres = dwdiag.exec_()
        if not diagres: 
            return None
        return dwdiag.getInput()    
    
    def editDialog(self):
        params = self.model.getParams()
        editDiag = SDataDialog(params)
        val = editDiag.exec_()
        if not val: 
            return None
        return editDiag.getInput()
    
    def initIcon(self):
        return QPixmap("images/parameterIcon.png").scaledToHeight(50)

class ConnectorNode(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap("images/connectorIcon.png").scaledToHeight(10))
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def dropEvent(self, e):
        if isinstance(e.source(), ConnectorNode):
            e.droppedOn = self
            return self.parentWidget().dropEvent(e)

    def dragEnterEvent(self, event):
        event.accept()
        
    def dragMoveEvent(self, e):
        return self.parentWidget().dragMoveEvent(e)
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            drag.setMimeData(QMimeData())
            drag.setHotSpot(event.pos() - self.rect().topLeft())            
            drag.exec_(Qt.MoveAction)

    def globalPosition(self):
        connectionPoint = QPoint(self.pos())
        connectionPoint.setX(connectionPoint.x() + self.width()/2)
        connectionPoint.setY(connectionPoint.y() + self.height()/2)
        return self.parentWidget().mapToGlobal(connectionPoint)

class ConnectorsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        
    def initConnectors(self, parent, n):
        return [self.addConnector(parent) for i in range(n)]
    
    def addConnector(self, parent):
        c = ConnectorNode()
        self.addWidget(c)
        return c
        
    def removeConnector(self, w):
        self.removeWidget(w)
        w.deleteLater()
        w.close()
