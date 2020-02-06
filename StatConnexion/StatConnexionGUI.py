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
        
        self.parcourirPushButton = self.ui.parcourirPushButton
        self.parcourirPushButton.clicked.connect(self.selectionFichier)   
        
        self.exporterPushButton = self.ui.exporterPushButton
        self.exporterPushButton.clicked.connect(self.exporter)   
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
        dateMaximum = self.dateFinLineEdit.text()
        self.ui.resultatTextEdit.clear()
   
        if dateMinimum < dateMaximum:
            
            with open(self.chemin, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        
                next(spamreader, None)
                connexion = 0       
                connexionTotale = 0
                connexionTotaleSalle = 0
                PCCollege = []
                self.rowListe = []
                self.rowListe.append("<html>")
                self.rowListe.append("<head>")
                self.rowListe.append("</head>")
                self.rowListe.append("<body>")
                self.rowListe.append("<table><thead><tr><th>Machine Id</th><th>Etat</th><th>Utilisateur</th><th>Date</th><th>Heure</th></tr></thead><tbody>")
                
                for row in spamreader:
                    date = row[3]
                    pc = row[0]
                    
                    if dateMinimum <= date and dateMaximum >=  date and pc == PC:
                        self.rowListe.append("<tr><td>" + row[0] + "</td>" + "<td>" + row[1] + "</td>" + "<td>" + row[2] + "</td>"+ "<td>" + row[3] + "</td>"+ "<td>" + row[4] + "</td>"+ "</tr>")
                    #PC de la salle
                    if dateMinimum <= date and dateMaximum >=  date and pc == PC and row[1] == "1":
                        #print(row)
                        connexion = connexion + 1
                        
                    #Salle
                    if dateMinimum <= date and dateMaximum >=  date and row[1] == "1" and pc.split("-")[1] == Salle:
                        connexionTotaleSalle = connexionTotaleSalle + 1
                        nombrePC = self.pcComboBox.count()
                    
                    #College
                    if dateMinimum <= date and dateMaximum >=  date and row[1] == "1":
                        connexionTotale = connexionTotale + 1
                        PCCollege.append(row[0])
                        
                PCCollege = list(dict.fromkeys(PCCollege))
                nombrePCUtilisie = len(PCCollege)
                
                self.rowListe.append("</tbody></table></body></html>")
                

            
            self.bilan(connexion, dateMinimum, dateMaximum, PC, Salle, connexionTotale, connexionTotaleSalle, nombrePC, nombrePCUtilisie)
        
    def showCalendarDateDebut(self):
        self.calendar = calendarGUI.Calendar()
        self.calendar.signal.connect(self.dateDebutChoisi)
        
    def showCalendarDateFin(self):
        self.calendar = calendarGUI.Calendar()
        self.calendar.signal.connect(self.dateFinChoisi)
        
    def dateDebutChoisi(self, date):
        dateMaximum = self.dateFinLineEdit.text()
        if date < dateMaximum or dateMaximum == "":
            self.dateDebutLineEdit.setText(date)
        
    def dateFinChoisi(self, date):
        dateMinimum = self.dateDebutLineEdit.text()
        if date > dateMinimum or dateMinimum == "":
            self.dateFinLineEdit.setText(date)

    def quit(self):
        self.close()
        
    def finished(self):
        date = self.calendar.getDate()
        print(date)
        
    def setDateDebut(self, dateDebut):
        self.ui.dateDebutLineEdit.setText(dateDebut)
            
    def bilan(self, connexion, dateMinimum, dateMaximum, PC, Salle, connexionTotale, connexionTotaleSalle, nombrePC, nombrePCUtilisie):
        connexion = str(connexion)
        connexionTotale = str(connexionTotale)
        connexionTotaleSalle = str(connexionTotaleSalle)
        nombrePC = str(nombrePC)
        nombrePCUtilisie = str(nombrePCUtilisie)
        
        self.ui.resultatTextEdit.append("*----------------Infos College---------------*")
        self.ui.resultatTextEdit.append("Du : "+dateMinimum+" au : "+dateMaximum)
        self.ui.resultatTextEdit.append("Nombre De Connexion: "+connexionTotale)
        self.ui.resultatTextEdit.append("Nombre De PC utilise: "+nombrePCUtilisie)
                     
        self.ui.resultatTextEdit.append("")
        
        self.ui.resultatTextEdit.append("*------------------Infos Salle----------------*")
        self.ui.resultatTextEdit.append("Salle : "+Salle)
        self.ui.resultatTextEdit.append("Du : "+dateMinimum+" au : "+dateMaximum)
        self.ui.resultatTextEdit.append("Nombre de PC:"+nombrePC)
        self.ui.resultatTextEdit.append("Nombre De Connexion: "+connexionTotaleSalle)     
          
        self.ui.resultatTextEdit.append("")
        
        self.ui.resultatTextEdit.append("*------------------Infos PC------------------*")  
        self.ui.resultatTextEdit.append("PC : "+PC)
        self.ui.resultatTextEdit.append("Du : "+dateMinimum+" au : "+dateMaximum)
        self.ui.resultatTextEdit.append("Nombre De Connexion: "+connexion)
      
    def selectionFichier(self):
        self.cheminExportTemp = QFileDialog.getOpenFileName(self, 'Choisire Destination', '', '*.html')
        self.cheminExport = self.cheminExportTemp[0]
  
    def exporter(self):

        self.Export = open(self.cheminExport, "w")
        
        for row in self.rowListe:
            self.Export.write(row)
        
        self.Export.close()           
                
        
