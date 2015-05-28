from stanguinic.dialogs.Dialog import *
from stanguinic.dialogs.auxliary.FieldType import FieldType


class DataDialog(StanDialog):
    
    def __init__(self, values = None):
        fieldNames = [("Name", "name"), ("Type", "type")]
        fieldTypes = [FieldType.TEXT, FieldType.SINGLE_SELECT]
        fieldValues = [None, [("Integer", DataDialog.SIntSubGroup), 
                              ("Real", DataDialog.SRealSubGroup), 
                              ("Vector", DataDialog.SVectorSubGroup)]]
        
        values = values if values else {}
        
        # Default values for in and outdegree
        if 'indegree' not in values:
            values['indegree'] = 0
        if 'outdegree' not in values:
            values['outdegree'] = 1
            
        super().__init__(fieldNames, fieldTypes, fieldValues, values)
        
        self.inputFields["type"].currentIndexChanged.connect(self.updateSubgroup)
        self.updateSubgroup(self.inputFields["type"].currentIndex())
        
    def updateSubgroup(self, newIndex):
        self.clearSpecific()
        self.specificGroup(self.inputFields["type"].currentData())
        self.adjustSize()
        
    class SIntSubGroup(QVBoxLayout):
        names = []
        types = []
        values = []
        
    class SRealSubGroup:
        names = [("Distribution", 'distribution')]
        types = [FieldType.DISTRIBUTION]
        values = [None]
        
    class SVectorSubGroup:
        names = [("Element type", "vec.type"), ("Direction", "vec.direction")]
        types = [FieldType.SINGLE_SELECT, FieldType.SINGLE_SELECT]
        values = [[("Integer",None), ("Real",None)], [("Column",None), ("Row",None)]]
        
