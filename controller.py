#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vue import *
from model import *
from vue2 import *
from vue3 import *

class Controller():
    def __init__(self):
        self.model=Model()
        a=list()
        a.append("TEst")
        self.vue=FenetrePrincipale(self.model.readDirectory(),self.model.readSites(),self)
        self.vue.bouton0.bind("<Button-1>",self.openChoices)
        self.vue.bouton1.bind("<Button-1>",self.newSite)
        self.vue.bouton2.bind("<Button-1>",self.deleteSite)


    def run(self):
        print("HAHA")
        self.vue.fenetre.mainloop()

    def newSite(self,event):
        self.fenetreNouveauSite=FenetreInputSite(1)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmNewSite)

    def deleteSite(self,event):
        self.fenetreNouveauSite=FenetreInputSite(2)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmDeleteSite)

    def confirmDeleteSite(self,event):

        print(str(self.fenetreNouveauSite.inputBox.get()))
        self.model.supprimerSite(str(self.fenetreNouveauSite.inputBox.get()))
        self.fenetreNouveauSite.master.destroy()
        self.vue.fenetre.destroy()
        self.newController=Controller()
        self.newController.run()

    def confirmNewSite(self,event):
    #    print(str(self.fenetreNouveauSite.nomSite.get()))
    #    print(str(self.fenetreNouveauSite.nomSite))
    #    print(str(self.fenetreNouveauSite.inputBox))
        print(str(self.fenetreNouveauSite.inputBox.get()))
    #    print("VOICI LA VALEUR DU TEXTE ENTRE DANS LA BOX "+ str(self.fenetreNouveauSite.nomSite))
        self.model.ajoutSite(str(self.fenetreNouveauSite.inputBox.get()))
        self.fenetreNouveauSite.master.destroy()
        self.vue.fenetre.destroy()
        self.newController=Controller()
        self.newController.run()


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
