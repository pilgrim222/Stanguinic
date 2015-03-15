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
    
    @staticmethod
    def fromDictionary(parameters):
        d = SData()
        d.update(parameters)
        return d
    
    def update(self, parameters):
        self.name = parameters['name']
        
    def getParams(self):
        params = {}
        params['name'] = self.name
        return params