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
        self.vue.bouton0.bind("<Button-1>",self.beginExtraction)


    def run(self):
        self.vue.fenetre.mainloop()


    def beginExtraction(self,event):
        print("HAHAHAHAHHAHA")
        self.model.readCSV(str(self.vue.listeCSV.get()))
