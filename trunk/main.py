
__author__="ggarri"
__date__ ="$17-Mar-2011 02:00:57$"

from controler import *
from gui.mainWindow import *

import sys

if __name__ == "__main__":

   app = QtGui.QApplication(sys.argv)

   wind = MainWindow()

   sys.exit(app.exec_())
   