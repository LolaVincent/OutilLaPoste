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
            self.labelEnonce=Label(self.master, text="Entrez le nom du nouveau site")
            self.labelEnonce.grid(row=0,column=0)
            self.nomSite=StringVar()
            self.inputBox=Entry(self.master,textvariable=self.nomSite)
            self.inputBox.grid(row=1,column=0)
            self.bouton=Button(self.master, text="Valider")
            self.bouton.grid(row=2,column=0)
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
