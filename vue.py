#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
from tkMessageBox import *



class FenetrePrincipale :
    def __init__(self,listeFichiers,listeSites,controller):
        self.fenetre = Tk()
        self.controller=controller
        #self.fenetre.configure(bg="white")
        self.fenetre.minsize(600,400)
        self.fenetre.wm_title("Outil La Poste")
        self.menubar = Menu(self.fenetre)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Ajout d'un site", command=self.controller.newSiteV2)
        self.menu1.add_command(label="Suppression d'un site", command=self.controller.deleteSiteV2)
        self.menubar.add_cascade(label="Sites", menu=self.menu1)

        #self.menu2 = Menu(self.menubar, tearoff=0)
        #self.menu2.add_command(label="Date de la dernière utilisation du logiciel")
        #self.menubar.add_cascade(label="Historique", menu=self.menu2)

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="Ajouter une équipe",command= self.controller.confirmAddTeamStep1)

        self.menu3.add_command(label="Supprimer une équipe", command=self.controller.confirmSuppressTeamStep1)
        self.menubar.add_cascade(label="Equipes", menu=self.menu3)

        self.menu4 = Menu(self.menubar, tearoff=0)
        self.menu4.add_command(label="Ajouter une tournée", command=self.controller.confirmAddTourneeStep1)
        self.menu4.add_command(label="Supprimer une tournée", command=self.controller.confirmDeleteTourneeStep1)
        self.menu4.add_command(label="Modifier le nombre de tournées", command=self.controller.confirmModifyTourneesStep1)
        self.menubar.add_cascade(label="Tournées", menu=self.menu4)



        #self.menu5 = Menu(self.menubar, tearoff=0)
        #self.menu5.add_command(label="A propos")
        #self.menubar.add_cascade(label="Aide", menu=self.menu5)

        # Quel CSV a été sélectionné ?
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

        self.stockPeriods.append("Semaines")
        self.stockPeriods.append("Mois")
        self.stockPeriods.append("Trimestre")


        self.periodsSelect.set(self.stockPeriods[0])

        self.listePeriods	= Combobox(self.lP, textvariable = self.periodsSelect,  values = self.stockPeriods, state = 'readonly')
        self.listePeriods.grid()
    #    self.sp1=Spinbox(self.lP,from_=1, to_=12)
    #    self.sp2=Spinbox(self.lP, from_=1, to_=12)
    #    self.sp1.grid()
    #    self.sp2.grid()



        photo = PhotoImage(file="logo.png")

        #canvas = Canvas(self.fenetre)
        #canvas.create_image(0, 0, anchor=NW, image=photo)
        #canvas.grid(row=1,padx=500, column=3)

        self.l = LabelFrame(self.fenetre, text="Liste des sites")
        self.l.grid()
        self.listCheckButton=list()
        self.listVariableCheckButton=list()
        self.listTextCheckButton=list()
        self.listeSites=listeSites
        i=0
        for element in listeSites:
            variable_i=BooleanVar()
            bouton = Checkbutton(self.l, text=str(element), variable=variable_i)
            bouton.grid(row=i,column=0, sticky =W)
            self.listVariableCheckButton.append(variable_i)
            self.listTextCheckButton.append(str(element))
            self.listCheckButton.append(bouton)

            i=i+1

        self.bouton1=Button(self.l, text="Ajouter site")
        self.bouton1.grid(row=i+3,sticky ='nesw')
        self.bouton2=Button(self.l, text="Supprimer site")
        self.bouton2.grid(row=i+4,sticky ='nesw')
        self.bouton0=Button(self.l, text="Liste des indicateurs")
        self.bouton0.grid(row=i+5,sticky ='nesw')
        self.bouton3=Button(self.l, text="Liste des réclamations")
        self.bouton3.grid(row=i+6,sticky ='nesw')




        self.fenetre.config(menu=self.menubar)

    def callbackBis(self,numeroAction):
        if numeroAction==2:
            question=askyesno('Sauvegarde en PDF', 'Voulez vous sauvegarder tous les graphiques générés dans un seul fichier PDF ?')
            if question==1:
                self.controller.savePDF()
            if question==0:
                showinfo('Message de confirmation', 'Rien ne sera effectué')


    @staticmethod
    def callback(numeroAction):
        if numeroAction==1:
            showinfo('Message de confirmation', 'Le traitement du fichier a bien été effectué !')
        if numeroAction==3:
                showinfo('Message de confirmation', 'Les fichiers ont bien été enregistrés dans un PDF')
        if numeroAction==4:
            showinfo('Message de confirmation', "L'opération a été réalisée avec succès !")
        if numeroAction==5:
            showerror("Erreur de lancement", "Désolé, l'outil ne peut pas se lancer. Vérifiez bien que le dossier 'FichiersCSV' existe, et qu'il ne contienne que des fichiers encodés en utf-8")
        if numeroAction==6:
            showerror("Erreur d'exécution", "Désolé, une erreur est survenue durant l'exécution de la tâche demandée.")
