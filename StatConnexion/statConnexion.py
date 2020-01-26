from PyQt5 import QtWidgets, uic

import StatConnexionGUI
        
statConnexionApplication = QtWidgets.QApplication([])
window = StatConnexionGUI.StatConnexion()
statConnexionApplication.exec()