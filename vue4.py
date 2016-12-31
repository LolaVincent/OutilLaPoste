#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreInputNombreTournees:
    def __init__(self,nomSite,nombreEquipes,nombreTotalTournees):


        self.master = Tk()
        self.master.wm_title("Caractéristiques du site " + nomSite + ":")
        self.partieEquipe = LabelFrame(self.master, text="Nombre de tournées par équipe")
        self.partieEquipe.grid()
        self.spinboxTournees=list()
        self.nomSite=nomSite
        self.nombreEquipes=nombreEquipes
        self.nombreTotalTournees=nombreTotalTournees

        i=0
        while i<nombreEquipes:
            numeroEquipe=Label(self.partieEquipe, text="Equipe n°" + str(i) + ":")
            numeroEquipe.grid(row=i,column=0)
            nombreTournees=Spinbox(self.partieEquipe, from_=1, to_=10)
            nombreTournees.grid(row=i,column=1)
            champText=Label(self.partieEquipe, text="tournée(s)")
            champText.grid(row=i,column=2)
            self.spinboxTournees.append(nombreTournees)
            i=i+1
        self.confirmButton=Button(self.partieEquipe, text="Valider")
        self.confirmButton.grid(row=i+1)
