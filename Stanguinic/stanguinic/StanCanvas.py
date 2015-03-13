'''
Created on Mar 5, 2015

@author: pilgrim
'''

import sys

from PyQt5.QtWidgets import (QWidget, QApplication, QMenu, QAction, QHBoxLayout)
from stanguinic.ModelWidgets import DataWidget

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
        
    def createTestUI(self):
        self.resize(200,200)
        self.show()

    # Override - item dropped on canvas
    def dropEvent(self, event):
        event.source().processMove(event)
    
    # Override - item dragged onto canvas
    def dragEnterEvent(self, event):
        event.accept()
        
    # Override - item dragged over canvas
    def dragMoveEvent(self, event):
        event.source().processMove(event)
    
    # Handles right-clicks on canvas
    def contextMenuEvent(self, event):
        action = self.rcmenu.exec_(self.mapToGlobal(event.pos()))
        if action == self.actions['addData']:
            self.addData(event.pos())
    
    def createRightClickMenu(self):
        self.rcmenu = QMenu(self)
        addIconAction = QAction("Add data", self)
        self.actions['addData'] = addIconAction
        self.rcmenu.addAction(addIconAction)
        
    def addData(self, pos):
        dataObject = DataWidget.dialog()
        if not dataObject:
            return
        
        ic = DataWidget(self, dataObject['name'])
        self.dataWidgets.append(ic)
        ic.move(pos)
        ic.show()