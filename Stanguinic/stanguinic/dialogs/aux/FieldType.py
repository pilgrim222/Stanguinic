from enum import Enum

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, \
    QButtonGroup, QDialogButtonBox, QComboBox, QSpinBox, QWidget

class FieldType(Enum):
    NUMERIC = 1
    TEXT = 2
    SINGLE_SELECT = 3
    SPIN = 4
    DISTRIBUTION = 5 # To je malo nerodno...
    
    def constructInputField(self, choices=None, value=None):
        if self == FieldType.NUMERIC:
            return QLineEdit(value, None)
        elif self == FieldType.TEXT:
            return QLineEdit(value, None)
        elif self == FieldType.SINGLE_SELECT:
            cbox = QComboBox()
            for (v,c) in choices:
                cbox.addItem(v, c)
            cbox.setCurrentIndex([v for (v,c) in choices].index(value) if value else 0)
            return cbox
        elif self == FieldType.SPIN:
            spin = QSpinBox()
            spin.setValue(value if value else 0)
            return spin
        elif self == FieldType.DISTRIBUTION:
            return DistributionGroup()
    
    @staticmethod    
    def getFieldValue(field):
        if isinstance(field, QLineEdit): 
            return field.text()
        elif isinstance(field, QComboBox):
            return field.currentText()
        elif isinstance(field, QSpinBox):
            return field.value()
        


from stanguinic.dialogs.aux.Distribution import DistributionGroup