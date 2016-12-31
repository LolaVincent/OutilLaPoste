#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vue import *
from model import *
from vue2 import *
from vue3 import *
from vue4 import *
from vue5 import *

class Controller():
    def __init__(self):
        self.model=Model()
        self.vue=FenetrePrincipale(self.model.readDirectory(),self.model.readSites(),self)
        self.vue.bouton0.bind("<Button-1>",self.openChoices)
        self.vue.bouton1.bind("<Button-1>",self.newSite)
        self.vue.bouton2.bind("<Button-1>",self.deleteSite)



    def run(self):
        print("HAHA")
        self.vue.fenetre.mainloop()



    def newSiteV2(self):
        self.fenetreNouveauSite=FenetreInputSite(1)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmNewSiteStep1)


    def newSite(self,event):
        self.fenetreNouveauSite=FenetreInputSite(1)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmNewSiteStep1)


    def deleteSite(self,event):
        self.fenetreNouveauSite=FenetreInputSite(2)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmDeleteSite)

    def deleteSiteV2(self):
        self.fenetreNouveauSite=FenetreInputSite(2)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmDeleteSite)

    def confirmDeleteSite(self,event):

        print(str(self.fenetreNouveauSite.inputBox.get()))
        self.model.supprimerSite(str(self.fenetreNouveauSite.inputBox.get()))
        self.fenetreNouveauSite.master.destroy()
        self.vue.fenetre.destroy()
        self.newController=Controller()
        self.newController.run()

    def confirmNewSiteStep1(self,event):
    #    print(str(self.fenetreNouveauSite.nomSite.get()))
    #    print(str(self.fenetreNouveauSite.nomSite))
    #    print(str(self.fenetreNouveauSite.inputBox))
        print(str(self.fenetreNouveauSite.inputBox.get()))
    #    print("VOICI LA VALEUR DU TEXTE ENTRE DANS LA BOX "+ str(self.fenetreNouveauSite.nomSite))

        nomNouveauSite=str(self.fenetreNouveauSite.inputBox.get())
        nombreNouvellesEquipes=int(self.fenetreNouveauSite.sbNbEquipe.get())
        nombreNouvellesTournees=int(self.fenetreNouveauSite.sbNbTournee.get())
        self.fenetreConfig2NouveauSite=FenetreInputNombreTournees(nomNouveauSite,nombreNouvellesEquipes,nombreNouvellesTournees)
        self.fenetreConfig2NouveauSite.confirmButton.bind("<Button-1>",self.confirmNewSiteStep2)
        self.fenetreNouveauSite.master.destroy()

    def confirmNewSiteStep2(self,event):
        nomSite=self.fenetreConfig2NouveauSite.nomSite
        nombreEquipes=self.fenetreConfig2NouveauSite.nombreEquipes
        nombreTotalTournees=self.fenetreConfig2NouveauSite.nombreTotalTournees
        nombreTourneesParEquipe=list()
        ind=0
        while ind<len(self.fenetreConfig2NouveauSite.spinboxTournees):
            valeur=int(self.fenetreConfig2NouveauSite.spinboxTournees[ind].get())
            nombreTourneesParEquipe.append(valeur)
            ind=ind+1
        self.fenetreConfig3NouveauSite=FenetreInputNomsTournees(nomSite,nombreEquipes,nombreTotalTournees,nombreTourneesParEquipe)
        self.fenetreConfig3NouveauSite.confirmButton.bind("<Button-1>",self.confirmNewSiteStep3)
        self.fenetreConfig2NouveauSite.master.destroy()

    def confirmNewSiteStep3(self,event):
        nomsToutesTournees=list()

        i=0
        nomSite=self.fenetreConfig3NouveauSite.nomSite
        nombreTotalTournees=self.fenetreConfig3NouveauSite.nombreTotalTournees

        while i < len(self.fenetreConfig3NouveauSite.nomsTourneesEquipes):
            j=0
            nomsTournees=list()
            while j < len(self.fenetreConfig3NouveauSite.nomsTourneesEquipes[i]):
                unNom=str(self.fenetreConfig3NouveauSite.nomsTourneesEquipes[i][j].get())
                nomsTournees.append(unNom)
                j=j+1
            nomsToutesTournees.append(nomsTournees)
            i=i+1
        print(nomsToutesTournees)
        self.model.ajoutSite(nomSite,nombreTotalTournees,nomsToutesTournees)
        self.fenetreConfig3NouveauSite.master.destroy()
        self.vue.fenetre.destroy()
        self.newController=Controller()
        self.newController.run()






        #self.model.ajoutSite(str(self.fenetreNouveauSite.inputBox.get()))
        #self.fenetreNouveauSite.master.destroy()
        #self.vue.fenetre.destroy()
        #self.newController=Controller()
        #self.newController.run()


    def openChoices(self,event):
        periodeChoisie=str(self.vue.listePeriods.get())
        self.fenetreChoix=FenetreInput(self.vue,periodeChoisie,self)
        self.fenetreChoix.bouton.bind("<Button-1>",self.beginExtraction)

    def beginExtraction(self,event):
        print("HAHAHAHAHHAHA")
        i=0
        listSites=list()
        #Là on est capable de voir la liste des boutons cochés  et de récupérer les sites sélectionnés
        while (i<len(self.vue.listVariableCheckButton)):
            if self.vue.listVariableCheckButton[i].get()==True:
                print(self.vue.listTextCheckButton[i])
                listSites.append(self.vue.listTextCheckButton[i])
            i=i+1
        print("VOICI LE CONTENU DE LA COMBO BOX : " + self.vue.listePeriods.get())
        if str(self.vue.listePeriods.get())=="Semaines":
            a=str(self.fenetreChoix.sbSemaines1.get())
            b=str(self.fenetreChoix.sbSemaines2.get())
            periodeEntree=a+'-'+b
        if str(self.vue.listePeriods.get())=="Mois":
            periodeEntree=str(self.fenetreChoix.sbMois.get())

        self.model.readCSV(str(self.vue.listeCSV.get()),listSites,str(self.vue.listePeriods.get()),periodeEntree)
        self.fenetreChoix.master.destroy()
        self.vue.callback(1)
        self.vue.callback(2)
        self.vue.fenetre.destroy()
        self.newController=Controller()
        self.newController.run()


    def savePDF(self):
        self.model.fromPNGToPDF("Résumé",self.model.listeImagesDossier("Graphiques/"), "Graphiques")
        self.vue.callback(3)
