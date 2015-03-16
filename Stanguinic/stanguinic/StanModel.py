'''
Created on Mar 5, 2015

@author: pilgrim
'''

class StanModel:
    def __init__(self):
        self.data = {}
        self.parameters = {}

    def addData(self, id, data):
        self.data[id] = data


class SData:
    def __init__(self):
        self.name = None
        self.type = None # To bo postalo odvec -- naj bo razvidno iz classa!
    
    @staticmethod
    def fromDictionary(parameters):
        d = SData()
        d.update(parameters)
        return d
    
    def update(self, parameters):
        self.name = parameters['name']
        self.type = parameters['type']
        
    def getParams(self):
        params = {}
        params['name'] = self.name
        params['type'] = self.type
        return params
    
    class SInt:
        def __init__(self):
            super().__init__()
    
    class SReal:
        def __init__(self):
            super().__init__()
            
    class SVector:
        def __init__(self):
            super().__init__()
    
    #... Tle gremo dalje se ostalo
    
    