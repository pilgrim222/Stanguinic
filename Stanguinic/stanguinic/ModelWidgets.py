'''
Created on Mar 11, 2015

@author: pilgrim
'''

from PyQt5.Qt import QPixmap
from PyQt5.QtCore import Qt, QMimeData, QSize, QEvent, QPoint
from PyQt5.QtGui import QDrag, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QGridLayout, QVBoxLayout, QFrame, QLayout, QSizePolicy
from stanguinic.StanModel import SParameter
import stanguinic.StanModel as StanModel
from stanguinic.dialogs.DataDialog import DataDialog


class QMoveableIconLabel(QWidget):
    '''
    General class which functions as an icon + text with the ability
    to drag & drop it around its parent widget.
    The parent widget should call the processMove function on drop event.
    
    '''    
    def __init__(self, parent):
        super().__init__(parent)
        self.indegree = 0
        self.outdegree = 0
        self.inConnectors = []
        self.outConnectors = []
        
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
        
    # By default forwards drops to be handled at the widget's parent
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
        self.inConnectors = self._left.initConnectors(self, self.indegree, True)
        self._right = ConnectorsLayout()
        self.outConnectors = self._right.initConnectors(self, self.outdegree, False) 
    
    def addInConnector(self):
        self.inConnectors.append(self._left.addConnector(self, True))
        self.indegree = self.indegree + 1
        
    def addOutConnector(self):
        self.outConnectors.append(self._right.addConnector(self, False))
        self.outdegree = self.outdegree + 1
    
    # Complicated due to connector handling (adding and removing)
    # Is there a more elegant solution? (Besides putting the connector handling
    # in another function?
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
        dwdiag = DataDialog()
        diagres = dwdiag.exec_()
        if not diagres: 
            return None
        return dwdiag.getInput()    
    
    def editDialog(self):
        params = self.model.getParams()
        editDiag = DataDialog(params)
        val = editDiag.exec_()
        if not val: 
            return None
        return editDiag.getInput()
    
    def initIcon(self):
        return QPixmap("images/parameterIcon.png").scaledToHeight(50)

class ConnectorNode(QLabel):
    def __init__(self, parent=None, isInput=False):
        super().__init__(parent)
        self.setPixmap(QPixmap("images/connectorIcon.png").scaledToHeight(10))
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.isInput = isInput
        self.connections = 0
    
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
    
    def validDrop(self, other):
        return not self.full() and not other.full() and self.isInput != other.isInput
    
    def full(self):
        return self.isInput and self.connections > 0

class ConnectorsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        
    def initConnectors(self, parent, n, isInput):
        return [self.addConnector(parent, isInput) for i in range(n)]
    
    def addConnector(self, parent, isInput):
        c = ConnectorNode(parent=parent, isInput=isInput)
        self.addWidget(c)
        return c
        
    def removeConnector(self, w):
        self.removeWidget(w)
        w.deleteLater()
        w.close()

class ConnectorLine:
    def __init__(self, c1, c2):
        if c1.isInput:
            self.start = c2
            self.end = c1
        else:
            self.start = c1
            self.end = c2
    
    def startsWith(self, c):
        return self.start == c

    def endsWith(self, c):
        return self.end == c
    