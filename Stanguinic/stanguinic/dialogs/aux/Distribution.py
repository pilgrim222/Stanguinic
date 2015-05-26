from FieldType import FieldType

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

class Distribution:
    def __init__(self, text="", parameters=[], param_names=[], param_types=[],
                 equation=""):
        self.text = text
        self.parameters = parameters
        self.param_names = param_names
        self.param_types = param_types
        self.equation = equation

class DistributionGroup:
        
    def __init__(self):
        pass
    
    
