#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreInput:
    def __init__(self,fenetreP,choixFait,controller,periodeMinMax):

        self.master = Tk()
        self.master.wm_title("Intervalle de temps considéré")
        if choixFait=="Mois":
            if periodeMinMax[0]==periodeMinMax[1]:
                self.sbMois=Spinbox(self.master, values=periodeMinMax)
            else:
                self.sbMois=Spinbox(self.master, from_=int(periodeMinMax[0]), to_=int(periodeMinMax[1]))

            self.labelMois=Label(self.master, text="Choisissez un mois entre 1 et 12")
            self.labelMois.grid(row=0,column=0)
            print(periodeMinMax[0])
            print(periodeMinMax[0])
            self.sbMois.grid(row=0,column=1)
        if choixFait=="Semaines":
            self.labelSemaines=Label(self.master, text="Choisissez un  intervalle de semaine de type a-b (avec a<=b)")
            self.labelSemaines.grid(row=0,column=0)
            self.sbSemaines1=Spinbox(self.master, from_=int(periodeMinMax[0]), to_=int(periodeMinMax[1]))
            self.sbSemaines2=Spinbox(self.master, from_=int(periodeMinMax[0]), to_=int(periodeMinMax[1]))
            self.sbSemaines1.grid(row=0,column=1)
            self.sbSemaines2.grid(row=0,column=2)


        if choixFait=="Trimestre":
            self.labelTrim=Label(self.master, text="Choisissez un trimestre entre 1 et 4")
            self.labelTrim.grid(row=0,column=0)
            self.sbTrim=Spinbox(self.master, from_=int(periodeMinMax[0]), to_=int(periodeMinMax[1]))
            self.sbTrim.grid(row=0,column=1)

        self.bouton=Button(self.master, text="Valider")
        self.bouton.grid(row=1,column=1)
