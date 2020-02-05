from PyQt5 import QtWidgets, uic
from PyQt5.Qt import QFileDialog

import csv
import calendarGUI

from builtins import dict

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
        
        self.resultatTextEdit = self.ui.resultatTextEdit
                
        self.show()
        
        
    def statConnexionFilePushButtonPressed(self):
        self.salleComboBox.clear()
        
        cheminTemp = QFileDialog.getOpenFileName(self, 'Choisir College', '', '*.csv')
        self.chemin = cheminTemp[0]
        self.statConnexionFileLineEdit.setText(self.chemin)
        
        listeSalle = []
        numSalle = []

        
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
        dateMinimum =  self.dateDebutLineEdit.text()
        dateMaximun = self.dateFinLineEdit.text()
        self.filtre(Salle, PC, dateMinimum, dateMaximun)
        
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
    
    def filtre(self, Salle, PC, dateMinimum, dateMaximum):
        
        if dateMinimum < dateMaximum:
            
            listeConnexionDate = []
            listeConnexionPC = []
            
            with open(self.chemin, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        
                next(spamreader, None)
                
                connexion = 0
                for row in spamreader:
                    date = row[3]
                    pc = row[0]
                    
                    if date >= dateMinimum and date <=  dateMaximum and pc == PC and row[1] == "1":
                            print(row)
                            connexion = connexion + 1
            print(connexion, dateMinimum, dateMaximum,PC)
            self.bilan(connexion, dateMinimum, dateMaximum, PC)
            
    def bilan(self, connexion, dateMinimum, dateMaximum, PC):        
        self.ui.resultatTextEdit.setText("PC : "+PC)
        #self.ui.resultatTextEdit.setText("Date Debut : "+dateMinimum)
        #self.ui.resultatTextEdit.setText("Date Fin : "+dateMaximum)
        #self.ui.resultatTextEdit.setText("Nombre de Connexion totale : "+connexion)   
