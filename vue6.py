#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreModifySite:
    def __init__(self,listeSites):
        self.master = Tk()
        self.master.wm_title("Ajout d'équipes à un site")
        self.labelEnonceSite=Label(self.master, text="Nom du site à modifier:")
        self.labelEnonceSite.grid(row=0,column=0)
        self.sitesSelect=StringVar()
        self.stockSites	=list()

        for element in listeSites:
            self.stockSites.append(str(element))
        self.sitesSelect.set(self.stockSites[0])
        self.listeSites	= Combobox(self.master, textvariable = self.sitesSelect,  values = self.stockSites, state = 'readonly')
        self.listeSites.grid(row=0,column=1)
        self.labelEnonceEquipe=Label(self.master, text="Nombre de nouvelles équipes pour ce site:")
        self.labelEnonceEquipe.grid(row=1,column=0)
        self.sbNbEquipe=Spinbox(self.master, from_=1, to_=10)
        self.sbNbEquipe.grid(row=1,column=1)
        self.bouton=Button(self.master, text="Valider")
        self.bouton.grid(row=2,column=1)
