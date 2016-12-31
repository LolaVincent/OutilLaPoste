#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *

class FenetreInputNomsTournees:
    def __init__(self,nomSite,nombreEquipes,nombreTotalTournees,nombreTourneesSurEquipe):


        self.master = Tk()
        self.master.wm_title("Caractéristiques des  " + nomSite + ":")
        self.partieEquipe = LabelFrame(self.master, text="Noms des tournées")
        self.partieEquipe.grid()
        self.nomsTourneesEquipes=list()
        self.nomSite=nomSite
        self.nombreEquipes=nombreEquipes
        self.nombreTotalTournees=nombreTotalTournees
        self.nombreTourneesSurEquipe=nombreTourneesSurEquipe

        i=0

        print(nombreTourneesSurEquipe)
        print("Le nombre d'équipes est")
        print(nombreEquipes)
        while i<nombreEquipes:
            print("La valeur de i est ")
            print(i)
            nomsChaqueTournee=list()
            print("la valeur de nombreTourneesSurEquipe[i] est ")
            print(nombreTourneesSurEquipe[i])
            partieTournee=LabelFrame(self.partieEquipe,text="Equipe n°"+ str(i))
            partieTournee.grid()
            j=0
            while j<nombreTourneesSurEquipe[i]:
                print("la valeur de j est")
                print(j)
                nomTournee=StringVar()
                inputBoxTournee=Entry(partieTournee,textvariable=nomTournee)
                inputBoxTournee.grid()
                nomsChaqueTournee.append(inputBoxTournee)
                j=j+1

            self.nomsTourneesEquipes.append(nomsChaqueTournee)
            i=i+1



        self.confirmButton=Button(self.partieEquipe, text="Valider")
        self.confirmButton.grid()
