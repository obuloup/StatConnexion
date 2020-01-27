from PyQt5 import QtWidgets, uic


class Calendar(QtWidgets.QMainWindow):
    def __init__(self):
        super(Calendar, self).__init__()
        self.ui = uic.loadUi("dialogueSelectionDate.ui", self)
        self.show()