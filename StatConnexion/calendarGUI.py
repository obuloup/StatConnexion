from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import pyqtSignal


class Calendar(QtWidgets.QMainWindow):
    
    signal = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super(Calendar, self).__init__()
        
        self.ui = uic.loadUi("dialogueSelectionDate.ui", self)
        
        self.calendarWidget = self.findChild(QtWidgets.QCalendarWidget, 'calendarWidget')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.quit)
        
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.show()
        
    def accept(self):
        self.date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.signal.emit(self.date)
        self.close()
    
    def quit(self):
        self.close()
