from PyQt5 import QtWidgets, uic


class Calendar(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Calendar, self).__init__()
        self.ui = uic.loadUi("dialogueSelectionDate.ui", self)
        
        self.calendarWidget = self.findChild(QtWidgets.QCalendarWidget, 'calendarWidget')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.quit)
        
        self.show()
        
    def accept(self):
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        print(date)
        self.close()
    
    def quit(self):
        self.close()