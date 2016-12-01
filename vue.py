#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *

class FenetrePrincipale :
    def __init__(self,listeFichiers):
        print('Constructiion dut truc')
        self.fenetre = Tk()
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

        # bouton de sortie
        bouton0=Button(self.fenetre, text="Valider")
        bouton0.grid(row=0, column=2)

        self.fenetre.config(menu=self.menubar)
        self.fenetre.mainloop()
