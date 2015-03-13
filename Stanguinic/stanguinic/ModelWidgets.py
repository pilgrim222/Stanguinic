'''
Created on Mar 11, 2015

@author: pilgrim
'''

from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QIcon
from stanguinic.StanDialog import StanDialog, FieldType
from PyQt5.Qt import QPixmap


class QMoveableIconLabel(QWidget):
    '''
    General class which functions as a QLabel (at the moment) with the ablity
    to drag & drop it around its parent widget.
    The parent widget should call the processMove function on drop event.
    '''
    def mouseMoveEvent(self, event):
        # If drag with left button:
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            drag.setMimeData(QMimeData())
            drag.setHotSpot(event.pos() - self.rect().topLeft())            
            drag.exec_(Qt.MoveAction)
            #self.moveDelta = event.pos() - self.pos()
    
    def processMove(self, dropEvent):
        #self.move(dropEvent.pos() + self.moveDelta)
        self.move(dropEvent.pos())
        
        
class DataWidget(QMoveableIconLabel):
    
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        
        iconPart = QLabel()
        textPart = QLabel(text)
        iconPart.setPixmap(self.initIcon())
        textPart.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout().addWidget(iconPart)
        self.layout().addWidget(textPart)
    
    # Right-click menu stub    
    def contextMenuEvent(self, event):
        pass
    
    # Prompt user for new data item specification (static)
    @staticmethod
    def dialog():
        dwdiag = StanDialog([("Name", "name")], [FieldType.TEXT], [None])
        diagres = dwdiag.exec_()
        if not diagres: 
            return None
         
        return dwdiag.getInput()
    
    def initIcon(self):
        return QPixmap("images/dataIcon.png").scaledToHeight(50)