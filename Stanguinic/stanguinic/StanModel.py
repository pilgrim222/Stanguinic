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
        

class SBase:
    def __init__(self):
        self.name = None
        self.indegree = 0
        self.outdegree = 0
        
    def getParams(self):
        a = {}
        a['name'] = self.name
        a['indegree'] = self.indegree
        a['outdegree'] = self.outdegree
        return a

    def update(self, params):
        self.name = params['name']
        self.indegree = params['indegree']
        self.outdegree = params['outdegree']

class SData(SBase):
    def __init__(self):
        super().__init__()
        self.type = None # To bo postalo odvec -- naj bo razvidno iz classa!
    
    @staticmethod
    def fromDictionary(parameters):
        d = SData()
        d.update(parameters)
        return d
    
    def update(self, parameters):
        super().update(parameters)
        self.name = parameters['name']
        self.type = parameters['type']
        
    def getParams(self):
        params = super().getParams()
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
    
    #... Tle gremo dalje se ostalo - bolj pametno: izven main classa in deduj iz SData
    # Gnezdenje classov namreč samo po sebi nima nobenega pomena.

class SParameter:
    def __init__(self):
        self.name = None
        self.type = None
        
    @staticmethod
    def fromDictionary(parameters):
        pass
    