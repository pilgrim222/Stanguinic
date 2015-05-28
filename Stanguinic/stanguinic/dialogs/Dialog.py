'''
Created on 13. mar. 2015

@author: pilgrim
'''

from PyQt5.Qt import QLabel, QHBoxLayout, QPalette, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, \
    QButtonGroup, QDialogButtonBox, QComboBox, QSpinBox, QWidget
from stanguinic.StanModel import SData
    from stanguinic.dialogs.auxiliary.FieldType import FieldType


class InputGroup(QWidget):
    """
    Holds a QLabel (property name) + input field
    """     
    
    def __init__(self, name, label, field):
        super().__init__()
        self.label = label
        self.field = field
        self.name = name
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().addWidget(QLabel(label))
        self.layout().addWidget(field)
        
    def delete(self):
        self.deleteLater()
        self.close()

class StanDialog(QDialog):

    def __init__(self, optionNames, optionTypes, optionValues, values=None):
        super().__init__()
        self.inputFields = {}
        self.setLayout(QVBoxLayout())
        
        for (dn,n),t,v in zip(optionNames, optionTypes, optionValues):
            self.inputFields[n] = t.constructInputField(v, values[n] if n in values else None)
            self.layout().addWidget(InputGroup(n, dn, self.inputFields[n]))
        
        self.layout().addLayout(self.connectorsGroup(values))
        self.specificOptions = QVBoxLayout()
        self.layout().addLayout(self.specificOptions)      
        self.layout().addWidget(self.confirmCancelButtonGroup())
        
    
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
        
        layout.addWidget(InputGroup("indegree", "Inputs", self.inputFields['indegree']))
        layout.addWidget(InputGroup("outdegree", "Outputs", self.inputFields['outdegree']))
        
        return layout
    
    def specificGroup(self, specClass, values={}):
        for (hn, n), t, v in zip(specClass.names, specClass.types, specClass.values):
            self.inputFields[n] = t.constructInputField(v, values[n] if n in values else None)
            self.specificOptions.addWidget(InputGroup(n, hn, self.inputFields[n]))
            
    def clearSpecific(self):
        for i in range(self.specificOptions.count()):
            e = self.specificOptions.takeAt(0)
            del self.inputFields[e.widget().name]
            e.widget().delete()
    
    def getInput(self):
        inputs = {}
        for f in self.inputFields.keys():
            inputs[f] = FieldType.getFieldValue(self.inputFields[f])
        return inputs
    
