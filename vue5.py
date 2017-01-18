#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreInputNomsTournees:
    def __init__(self,nomSite,nombreEquipes,nombreTotalTournees,nombreTourneesSurEquipe):


        self.master = Tk()
        if nombreTotalTournees==0:
            self.master.wm_title("Noms des nouvelles tournées de  " + nomSite + ":")
        if nombreTotalTournees!=0:
            self.master.wm_title("Noms des tournées de  " + nomSite + ":")



        self.partieEquipe = LabelFrame(self.master, text="Noms des tournées")
        self.partieEquipe.grid()
        self.nomsTourneesEquipes=list()
        self.nomSite=nomSite
        self.nombreEquipes=nombreEquipes
        self.nombreTotalTournees=nombreTotalTournees
        self.nombreTourneesSurEquipe=nombreTourneesSurEquipe

        i=0


        while i<int(nombreEquipes):

            nomsChaqueTournee=list()


            partieTournee=LabelFrame(self.partieEquipe,text="Equipe n°"+ str(i+1))
            partieTournee.grid()
            j=0
            while j<nombreTourneesSurEquipe[i]:
                nomTournee=StringVar()
                inputBoxTournee=Entry(partieTournee,textvariable=nomTournee)
                inputBoxTournee.grid()
                nomsChaqueTournee.append(inputBoxTournee)
                j=j+1

            self.nomsTourneesEquipes.append(nomsChaqueTournee)
            i=i+1



        self.confirmButton=Button(self.partieEquipe, text="Valider")
        self.confirmButton.grid()
