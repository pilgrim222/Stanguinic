'''
Created on 13. mar. 2015

@author: pilgrim
'''
import sys

from PyQt5.QtWidgets import QApplication
from stanguinic.StanCanvas import StanCanvas


if __name__ == '__main__':
    app = QApplication(sys.argv)    
    mainWindow = StanCanvas()
    sys.exit(app.exec_())