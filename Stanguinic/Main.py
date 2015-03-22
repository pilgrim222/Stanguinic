'''
Created on 13. mar. 2015

@author: pilgrim
'''
from stanguinic.StanCanvas import StanCanvas
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)    
    mainWindow = StanCanvas()
    sys.exit(app.exec_())