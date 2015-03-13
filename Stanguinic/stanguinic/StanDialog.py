'''
Created on 13. mar. 2015

@author: pilgrim
'''
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton,\
    QButtonGroup, QDialogButtonBox
from PyQt5.Qt import QLabel, QHBoxLayout

from enum import Enum
from PyQt5.QtCore import Qt

class FieldType(Enum):
    NUMERIC = 1
    TEXT = 2
    SINGLE_SELECT = 3
    
    def constructInputField(self, values=None):
        if self == FieldType.NUMERIC:
            return QLineEdit()
        elif self == FieldType.TEXT:
            return QLineEdit()
        #... manjka
    
    @staticmethod    
    def getFieldValue(field):
        if isinstance(field, QLineEdit): 
            return field.text()
    
class StanDialog(QDialog):

    def __init__(self, optionNames, optionTypes, optionValues):
        super().__init__()
        self.inputFields = {}
        self.setLayout(QVBoxLayout())
        
        for (dn,n),t,v in zip(optionNames, optionTypes, optionValues):
            self.inputFields[n] = t.constructInputField(v)
            self.layout().addLayout(self.constructGroup(dn, self.inputFields[n]))
        
        self.layout().addWidget(self.confirmCancelButtonGroup())
    
    def constructGroup(self, name, field):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name))
        layout.addWidget(field)
        return layout
    
    def confirmCancelButtonGroup(self):
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        return buttons
    
    def getInput(self):
        inputs = {}
        for f in self.inputFields.keys():
            inputs[f] = FieldType.getFieldValue(self.inputFields[f])
        return inputs