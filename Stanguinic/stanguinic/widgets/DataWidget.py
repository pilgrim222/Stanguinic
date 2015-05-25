from stanguinic.ModelWidgets import QMoveableIconLabel
from stanguinic.StanModel import SData
from stanguinic.dialogs.DataDialog import DataDialog
from PyQt5.Qt import QPixmap

class DataWidget(QMoveableIconLabel):
    
    def __init__(self, parent, parameters):
        super().__init__(parent)
        self.id = parameters['name']
        self.createVisual(parameters)
        self.model = SData.fromDictionary(parameters)
        
    def updateParams(self, newParams):
        self.model.update(newParams)
    
    def mouseDoubleClickEvent(self, event):
        newparams = self.editDialog()
        if not newparams:
            return
        self.updateVisual(newparams)
        self.model.update(newparams)
    
    # Prompt user for new data item specification (static)
    @staticmethod
    def createDialog():
        dwdiag = DataDialog()
        diagres = dwdiag.exec_()
        if not diagres: 
            return None
        return dwdiag.getInput()    
    
    def editDialog(self):
        params = self.model.getParams()
        editDiag = DataDialog(params)
        val = editDiag.exec_()
        if not val: 
            return None
        return editDiag.getInput()
    
    def initIcon(self):
        return QPixmap("images/dataIcon.png").scaledToHeight(50)
    