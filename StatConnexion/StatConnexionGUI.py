from PyQt5 import QtWidgets, uic
from PyQt5.Qt import QFileDialog

import csv
from builtins import dict

class StatConnexion(QtWidgets.QMainWindow):
    def __init__(self):
        super(StatConnexion, self).__init__()
        self.ui = uic.loadUi("StatConnexion.ui", self)
        
        self.statConnexionFilePushButton = self.findChild(QtWidgets.QPushButton, 'statConnexionFilePushButton')
        self.statConnexionFilePushButton.clicked.connect(self.statConnexionFilePushButtonPressed)
        
        self.statConnexionFileLineEdit = self.ui.statConnexionFileLineEdit
        
        self.salleComboBox = self.ui.salleComboBox
        self.pcComboBox = self.ui.pcComboBox
        
        self.show()
        
        
    def statConnexionFilePushButtonPressed(self):
        
        chemin = QFileDialog.getOpenFileName(self, 'Choisir College', '', '*.csv')
        self.statConnexionFileLineEdit.setText(chemin[0])
        
        listeSalle = []
        numSalle = []
        ListeFinaleSalle = []
        
        listePC = []
        ListeFinalePC =[]
        
        with open(chemin[0], newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    
            next(spamreader, None)
    
            for row in spamreader:
                infoPC = row[0]
                listeSalle.append(infoPC.split("-"))
                listePC.append(infoPC)
    
            for row in listeSalle:
                numeroSalle = row[1]
                numSalle.append(numeroSalle)
        
        numSalle = list(dict.fromkeys(numSalle))
        listePC = list(dict.fromkeys(listePC))
        
        self.salleComboBox.addItems(numSalle)
        self.pcComboBox.addItems(listePC)
        
        # Traitement du fichier csv
        
