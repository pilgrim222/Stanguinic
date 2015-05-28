from stanguinic.dialogs.aux.FieldType import FieldType
from PyQt5.QtWidgets import QVBoxLayout, QWidget

class Distribution:
    def __init__(self, text="", parameters=[], param_names=[], param_types=[],
                 equation=""):
        self.text = text
        self.parameters = parameters
        self.param_names = param_names
        self.param_types = param_types
        self.equation = equation

class DistributionGroup(QWidget):        
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        mainchoicel = QVBoxLayout()
        distChoice = FieldType.SINGLE_SELECT.constructInputField(choices = 
                                                [(v.text, v) for (k,v) in distributions.items()])
        mainchoicel.addWidget(distChoice)
        layout.addLayout(mainchoicel)
        self.setLayout(layout)
        
distributions = {
    'normal' : Distribution(
        text = 'Normal',
        parameters = ['mu', 'sigma'],
        param_names = ['mean', 'stddev'],
        param_types = [FieldType.NUMERIC, FieldType.NUMERIC],
        ),
    'poisson' : Distribution(
        text = 'Poisson',
        parameters = ['lambda'],
        param_names = ['lambda'],
        param_types = [FieldType.NUMERIC]
        ),
    }