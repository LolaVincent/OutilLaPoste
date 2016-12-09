#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vue import *
from model import *

class Controller():
    def __init__(self):
        self.model=Model()
        a=list()
        a.append("TEst")
        self.vue=FenetrePrincipale(self.model.readDirectory(),self.model.readSites(),self)
        self.vue.bouton0.bind("<Button-1>",self.openChoices)


    def run(self):
        self.vue.fenetre.mainloop()

    def openChoices(self,event):
        periodeChoisie=str(self.vue.stockPeriods.get())
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
        if str(self.vue.stockPeriods)=="Semaines":
            a=str(self.fenetreChoix.sbSemaines1.get())
            b=str(self.fenetreChoix.sbSemaines2.get())
            periodeEntree=a+'-'+b
        if str(self.vue.stockPeriods)=="Mois":
            periodeEntree=str(self.fenetreChoix.sbMois.get())

        self.model.readCSV(str(self.vue.listeCSV.get()),listSites,str(self.vue.stockPeriods),periodeEntree)
        self.fenetreChoix.master.destroy()
        self.vue.callback(1)
        self.vue.callback(2)
        self.vue.fenetre.destroy()
        self.vue=FenetrePrincipale(self.model.readDirectory(),self.model.readSites(),self)

    def savePDF(self):
        self.model.fromPNGToPDF("Résumé",self.model.listeImagesDossier("Graphiques/"), "Graphiques")
        self.vue.callback(3)
