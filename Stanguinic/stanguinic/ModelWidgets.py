'''
Created on Mar 11, 2015

@author: pilgrim
'''

import stanguinic.StanModel as StanModel

from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QIcon
from stanguinic.StanDialog import SDataDialog
from stanguinic.StanModel import SData
from PyQt5.Qt import QPixmap


class QMoveableIconLabel(QWidget):
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
    
    # Creates the default visual representation (icon with text underneath)
    # Needs the initIcon function to be implemented and return a QPixmap object
    # containing the icon.    
    def createVisual(self, name):
        self.setLayout(QVBoxLayout())
        self._iconPart = QLabel()
        self._textPart = QLabel(name)
        self._iconPart.setPixmap(self.initIcon())
        self._textPart.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout().addWidget(self._iconPart)
        self.layout().addWidget(self._textPart)
        
    def updateVisual(self, newParams):
        self._textPart.setText(newParams['name'])
        
class DataWidget(QMoveableIconLabel):
    
    def __init__(self, parent, parameters):
        super().__init__(parent)
        self.id = parameters['name']
        self.createVisual(parameters['name'])
        self.model = SData.fromDictionary(parameters)
        
    def updateParams(self, newParams):
        self.model.update(newParams)
        

    # Right-click menu stub    
    def contextMenuEvent(self, event):
        pass
    
    def mouseDoubleClickEvent(self, event):
        newparams = self.editDialog()
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
    pass