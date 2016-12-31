#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreInputSite:
    def __init__(self,typeEntree):

        if typeEntree==1:
            self.master = Tk()
            self.master.wm_title("Nouveau Site")
            self.labelEnonceSite=Label(self.master, text="Nom du nouveau site:")
            self.labelEnonceSite.grid(row=0,column=0)
            self.nomSite=StringVar()
            self.inputBox=Entry(self.master,textvariable=self.nomSite)
            self.inputBox.grid(row=0,column=1)
            self.labelEnonceEquipe=Label(self.master, text="Nombre d'équipes pour ce site:")
            self.labelEnonceEquipe.grid(row=1,column=0)
            self.sbNbEquipe=Spinbox(self.master, from_=1, to_=10)
            self.sbNbEquipe.grid(row=1,column=1)
            self.labelEnonceTournee=Label(self.master, text="Nombre de tournées pour ce site:")
            self.labelEnonceTournee.grid(row=2,column=0)
            self.sbNbTournee=Spinbox(self.master, from_=1, to_=10)
            self.sbNbTournee.grid(row=2,column=1)
            self.bouton=Button(self.master, text="Valider")
            self.bouton.grid(row=3,column=1)
        else:
            self.master = Tk()
            self.master.wm_title("Site à supprimer")
            self.labelEnonce=Label(self.master, text="Entrez le nom du site à supprimer")
            self.labelEnonce.grid(row=0,column=0)
            self.nomSite=StringVar()
            self.inputBox=Entry(self.master,textvariable=self.nomSite)
            self.inputBox.grid(row=1,column=0)
            self.bouton=Button(self.master, text="Valider")
            self.bouton.grid(row=2,column=0)
