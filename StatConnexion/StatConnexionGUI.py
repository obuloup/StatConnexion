from PyQt5 import QtWidgets, uic
from PyQt5.Qt import QFileDialog
from PyQt5.QtCore import pyqtSignal

import csv
import calendarGUI

from builtins import dict
from calendar import calendar

class StatConnexion(QtWidgets.QMainWindow):
    
    chemin = ''
    
    def __init__(self):
        
        super(StatConnexion, self).__init__()
        self.ui = uic.loadUi("StatConnexion.ui", self)
        
        self.statConnexionFilePushButton = self.findChild(QtWidgets.QPushButton, 'statConnexionFilePushButton')
        self.statConnexionFilePushButton.clicked.connect(self.statConnexionFilePushButtonPressed)
        
        self.statConnexionFileLineEdit = self.ui.statConnexionFileLineEdit
        
        self.salleComboBox = self.ui.salleComboBox
        self.pcComboBox = self.ui.pcComboBox
        
        self.salleComboBox.currentIndexChanged.connect(self.updatePC)
        
        self.quitPushButton = self.ui.quitPushButton
        self.quitPushButton.clicked.connect(self.quit)
        
        self.validationPushButton = self.ui.validationPushButton
        self.validationPushButton.clicked.connect(self.validate)
        
        self.dateDebutPushButton = self.ui.dateDebutPushButton
        self.dateDebutPushButton.clicked.connect(self.showCalendarDateDebut)
        
        self.dateFinPushButton = self.ui.dateFinPushButton
        self.dateFinPushButton.clicked.connect(self.showCalendarDateFin)
        
        self.dateDebutLineEdit = self.ui.dateDebutLineEdit
        self.dateFinLineEdit = self.ui.dateFinLineEdit
                
        self.show()
        
        
    def statConnexionFilePushButtonPressed(self):
        self.salleComboBox.clear()
        
        cheminTemp = QFileDialog.getOpenFileName(self, 'Choisir College', '', '*.csv')
        self.chemin = cheminTemp[0]
        self.statConnexionFileLineEdit.setText(self.chemin)
        
        listeSalle = []
        numSalle = []
        ListeFinaleSalle = []
        
        if self.chemin.strip() != "":
        
            with open(self.chemin, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        
                next(spamreader, None)
        
                for row in spamreader:
                    infoPC = row[0]
                    listeSalle.append(infoPC.split("-"))
        
                for row in listeSalle:
                    numeroSalle = row[1]
                    numSalle.append(numeroSalle)
            
            numSalle = list(dict.fromkeys(numSalle))
            
            self.salleComboBox.addItems(numSalle)
        
    def updatePC(self):
        self.pcComboBox.clear()
        
        Salle = self.salleComboBox.currentText()
        
        listePC = []
        ListeFinalePC =[]
        
        if self.chemin.strip() != "":
        
            with open(self.chemin, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        
                next(spamreader, None)
        
                for row in spamreader:
                    infoPC = row[0]
                    if infoPC.split("-")[1] == Salle: 
                        listePC.append(infoPC)
        
            listePC = list(dict.fromkeys(listePC))
            
            self.pcComboBox.addItems(listePC)
    
    def validate(self):
        Salle = self.salleComboBox.currentText()
        PC = self.pcComboBox.currentText()        
        print(Salle, PC)
        
    def showCalendarDateDebut(self):
        self.calendar = calendarGUI.Calendar()
        self.calendar.signal.connect(self.dateDebutChoisi)
        
    def showCalendarDateFin(self):
        self.calendar = calendarGUI.Calendar()
        self.calendar.signal.connect(self.dateFinChoisi)
        
    def dateDebutChoisi(self, date):
        self.dateDebutLineEdit.setText(date)
        
    def dateFinChoisi(self, date):
        self.dateFinLineEdit.setText(date)
            
        
    def quit(self):
        self.close()
        
    def finished(self):
        date = self.calendar.getDate()
        print(date)
        
    def setDateDebut(self, dateDebut):
        self.ui.dateDebutLineEdit.setText(dateDebut)
    