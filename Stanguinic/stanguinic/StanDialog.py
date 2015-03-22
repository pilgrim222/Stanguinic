'''
Created on 13. mar. 2015

@author: pilgrim
'''
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton,\
    QButtonGroup, QDialogButtonBox, QComboBox, QSpinBox
from PyQt5.Qt import QLabel, QHBoxLayout
from stanguinic.StanModel import SData

from enum import Enum
from PyQt5.QtCore import Qt

class FieldType(Enum):
    NUMERIC = 1
    TEXT = 2
    SINGLE_SELECT = 3
    SPIN = 4
    
    def constructInputField(self, choices=None, value=None):
        if self == FieldType.NUMERIC:
            return QLineEdit(value, None)
        elif self == FieldType.TEXT:
            return QLineEdit(value, None)
        elif self == FieldType.SINGLE_SELECT:
            cbox = QComboBox()
            for v in choices:
                cbox.addItem(v, 333)
            cbox.setCurrentIndex(choices.index(value) if value else 0)
            return cbox
        elif self == FieldType.SPIN:
            spin = QSpinBox()
            spin.setValue(value if value else 0)
            return spin
    
    @staticmethod    
    def getFieldValue(field):
        if isinstance(field, QLineEdit): 
            return field.text()
        elif isinstance(field, QComboBox):
            return field.currentText()
        elif isinstance(field, QSpinBox):
            return field.value()
    
class StanDialog(QDialog):

    def __init__(self, optionNames, optionTypes, optionValues, values=None):
        super().__init__()
        self.inputFields = {}
        self.setLayout(QVBoxLayout())
        
        for (dn,n),t,v in zip(optionNames, optionTypes, optionValues):
            self.inputFields[n] = t.constructInputField(v, values[n] if n in values else None)
            self.layout().addLayout(self.constructGroup(dn, self.inputFields[n]))
        
        self.layout().addLayout(self.connectorsGroup(values))
        
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
    
    def connectorsGroup(self, values=None):
        layout = QVBoxLayout()
        
        self.inputFields['indegree'] = FieldType.SPIN.constructInputField(None, values['indegree'] if values else 0)
        self.inputFields['outdegree'] = FieldType.SPIN.constructInputField(None, values['outdegree'] if values else 0)
        
        layout.addLayout(self.constructGroup("Inputs", self.inputFields['indegree']))
        layout.addLayout(self.constructGroup("Outputs", self.inputFields['outdegree']))
        
        return layout
    
    def getInput(self):
        inputs = {}
        for f in self.inputFields.keys():
            inputs[f] = FieldType.getFieldValue(self.inputFields[f])
        return inputs
    
class SDataDialog(StanDialog):    
    
    def __init__(self, values = None):
        fieldNames = [("Name", "name"), ("Type", "type")]
        fieldTypes = [FieldType.TEXT, FieldType.SINGLE_SELECT]
        fieldValues = [None, ["Integer", "Real"]]
        
        values = values if values else {}
        
        if 'indegree' not in values:
            values['indegree'] = 0
        if 'outdegree' not in values:
            values['outdegree'] = 1
        
        super().__init__(fieldNames, fieldTypes, fieldValues, values)        
    
        
    class SIntSubGroup(QVBoxLayout):
        def __init__(self):
            super().__init__()
    
    class SRealSubGroup(QVBoxLayout):
        def __init__(self):
            super().__init__()
    
    class SVectorSubGroup(QVBoxLayout):
        def __init__(self):
            super().__init__()            
            #FieldType.SINGLE_SELECT.constructInputField(choices, value)