#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreModifySite2:
    def __init__(self,nomSite,nombreEquipes):


        self.master = Tk()
        self.master.wm_title("Nouvelle(s) équipe(s) de " + nomSite + ":")
        self.partieEquipe = LabelFrame(self.master, text="Nombre de tournées par équipe")
        self.partieEquipe.grid()
        self.spinboxTournees=list()
        self.nomSite=nomSite
        self.nombreEquipes=nombreEquipes

        ind=0
        print("AVANT LA BOUCLE DE LA FENETRE")
        print("VOILA LA VALEUR DE NOMMBREEQUIPES")
        print(nombreEquipes)
        while (ind<int(nombreEquipes)):
            ind=ind+1
            print("DANS LA BOUCLE")
            print("VOILA LA VALEUR DE NOMMBREEQUIPES")
            print(nombreEquipes)
            print("VOILA LA VALEUR DE l'INDICE")
            print(ind)
            numeroEquipe=Label(self.partieEquipe, text="Equipe n°" + str(ind) + ":")
            numeroEquipe.grid(row=ind,column=0)
            nombreTournees=Spinbox(self.partieEquipe, from_=1, to_=10)
            nombreTournees.grid(row=ind,column=1)
            champText=Label(self.partieEquipe, text="tournée(s)")
            champText.grid(row=ind,column=2)
            self.spinboxTournees.append(nombreTournees)

        self.confirmButton=Button(self.partieEquipe, text="Valider")
        self.confirmButton.grid(row=ind+1)
