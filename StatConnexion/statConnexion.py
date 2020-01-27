from PyQt5 import QtWidgets, uic

import StatConnexionGUI
        
statConnexionApplication = QtWidgets.QApplication([])
StatConnexionGUI.StatConnexion()
statConnexionApplication.exec()