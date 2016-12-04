#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *


class FenetrePrincipale :
    def __init__(self,listeFichiers,listeSites,controller):
        print('Constructiion dut truc')
        self.fenetre = Tk()
        self.controller=controller
        #self.fenetre.configure(bg="white")
        self.fenetre.minsize(900,600)
        self.fenetre.wm_title("Outil La Poste")
        self.menubar = Menu(self.fenetre)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Ajout d'un site")
        self.menu1.add_command(label="Suppression d'un site")
        self.menubar.add_cascade(label="Sites", menu=self.menu1)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Date de la dernière utilisation du logiciel")
        self.menubar.add_cascade(label="Historique", menu=self.menu2)

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="Equipes")
        self.menu3.add_command(label="Tournées")
        self.menubar.add_cascade(label="Paramètres", menu=self.menu3)



        self.menu4 = Menu(self.menubar, tearoff=0)
        self.menu4.add_command(label="A propos")
        self.menubar.add_cascade(label="Aide", menu=self.menu4)

        # Quel fruit a été sélectionné ?
        self.cSVSelect	= StringVar()
        self.stockCSV	=list()

        for element in listeFichiers:
            self.stockCSV.append(str(element))
        self.cSVSelect.set(self.stockCSV[0])

        self.listeCSV	= Combobox(self.fenetre, textvariable = self.cSVSelect,  values = self.stockCSV, state = 'readonly')



		# Placement des widgets
        self.listeCSV.grid()

        self.periodsSelect	= StringVar()
        self.stockPeriods	=list()
        self.lP = LabelFrame(self.fenetre, text="Période traitée")
        self.lP.grid()


        self.stockPeriods.append("Mois")
        self.stockPeriods.append("Semaines")

        self.periodsSelect.set(self.stockPeriods[0])

        self.listePeriods	= Combobox(self.lP, textvariable = self.periodsSelect,  values = self.stockPeriods, state = 'readonly')
        self.listePeriods.grid()
        self.sp1=Spinbox(self.lP,from_=1, to_=12)
        self.sp2=Spinbox(self.lP, from_=1, to_=12)
        self.sp1.grid()
        self.sp2.grid()

        self.bouton0=Button(self.fenetre, text="Valider")
        self.bouton0.grid(row=0, column=2)

        photo = PhotoImage(file="logo.png")

        #canvas = Canvas(self.fenetre)
        #canvas.create_image(0, 0, anchor=NW, image=photo)
        #canvas.grid(row=1,padx=500, column=3)

        self.l = LabelFrame(self.fenetre, text="Liste des sites")
        self.l.grid()
        self.listCheckButton=list()
        self.listVariableCheckButton=list()
        self.listTextCheckButton=list()
        i=0
        for element in listeSites:
            variable_i=BooleanVar()
            bouton = Checkbutton(self.l, text=str(element), variable=variable_i)
            bouton.grid(row=i)
            self.listVariableCheckButton.append(variable_i)
            self.listTextCheckButton.append(str(element))
            self.listCheckButton.append(bouton)

            i=i+1

        self.bouton1=Button(self.l, text="Ajouter site")
        self.bouton1.grid(row=i+1)
        self.bouton2=Button(self.l, text="Supprimer site")
        self.bouton2.grid(row=i+2)



        self.fenetre.config(menu=self.menubar)




        
