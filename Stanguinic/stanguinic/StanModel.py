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
        
    def addParameter(self, id, parameter):
        self.parameters[id] = parameter
        

class SBase:
    def __init__(self):
        self.data = {}
        
    def getParams(self):
        return self.data

    def update(self, params):
        self.data.update(params)


########### DATA ##################
class SData(SBase):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def fromDictionary(parameters):
        d = SData()
        d.update(parameters)
        return d
    
class SInt(SData):
    def __init__(self):
        super().__init__()
    
class SReal(SData):
    def __init__(self):
        super().__init__()
            
class SVector(SData):
    def __init__(self):
        super().__init__()


############ PARAMETERS ###############   
class SParameter(SBase):
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def fromDictionary(parameters):
        d = SParameter()
        d.update(parameters)
        return d
    