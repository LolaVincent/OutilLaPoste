#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreInput:
    def __init__(self,fenetreP,choixFait,controller):

        self.master = Tk()
        if choixFait=="Mois":
            self.labelMois=Label(self.master, text="Choisissez un mois entre 1 et 12")
            self.labelMois.grid(row=0,column=0)
            self.sbMois=Spinbox(self.master, from_=1, to_=12)
            self.sbMois.grid(row=0,column=1)
        if choixFait=="Semaines":
            self.labelSemaines=Label(self.master, text="Choisissez un  intervalle de semaine de type a-b (avec a<=b) et b<4")
            self.labelSemaines.grid(row=0,column=0)
            self.sbSemaines1=Spinbox(self.master, from_=1, to_=4)
            self.sbSemaines2=Spinbox(self.master, from_=1, to_=4)
            self.sbSemaines1.grid(row=0,column=1)
            self.sbSemaines2.grid(row=0,column=2)


        if choixFait=="Trimestres"
            self.labelTrim=Label(self.master, text="Choisissez un trimestre entre 1 et 4")
            self.labelTrim.grid(row=0,column=0)
            self.sbTrim=Spinbox(self.master, from_=1, to_=4)
            self.sbTrim.grid(row=0,column=1)
