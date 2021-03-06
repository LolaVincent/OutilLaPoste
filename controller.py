#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vue import *
from model import *
from vue2 import *
from vue3 import *
from vue4 import *
from vue5 import *
from vue6 import *
from vue7 import *
from vue8 import *
from vue9 import *
from vue10 import *
from vue11 import *

class Controller():
    def __init__(self):
        self.model=Model()
        try:
            self.vue=FenetrePrincipale(self.model.readDirectory(),self.model.readSites(),self)
            self.vue.bouton0.bind("<Button-1>",self.openChoices)
            self.vue.bouton1.bind("<Button-1>",self.newSite)
            self.vue.bouton2.bind("<Button-1>",self.deleteSite)
            self.vue.bouton3.bind("<Button-1>",self.openChoicesRecla)
        except Exception:
            FenetrePrincipale.callback(5)




    def run(self):
        self.vue.fenetre.mainloop()



    def newSiteV2(self):
        self.fenetreNouveauSite=FenetreInputSite(1)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmNewSiteStep1)


    def newSite(self,event):
        self.fenetreNouveauSite=FenetreInputSite(1)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmNewSiteStep1)


    def deleteSite(self,event):
        self.fenetreNouveauSite=FenetreInputSite(2)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmDeleteSite)

    def deleteSiteV2(self):
        self.fenetreNouveauSite=FenetreInputSite(2)
        self.fenetreNouveauSite.bouton.bind("<Button-1>",self.confirmDeleteSite)

    def confirmDeleteSite(self,event):
        try:

            self.model.supprimerSite(str(self.fenetreNouveauSite.inputBox.get()))
            self.fenetreNouveauSite.master.destroy()
            FenetrePrincipale.callback(4)
        except Exception:
            self.fenetreNouveauSite.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()

    def confirmNewSiteStep1(self,event):
        nomNouveauSite=str(self.fenetreNouveauSite.inputBox.get())
        nombreNouvellesEquipes=int(self.fenetreNouveauSite.sbNbEquipe.get())
        nombreNouvellesTournees=int(self.fenetreNouveauSite.sbNbTournee.get())
        self.fenetreConfig2NouveauSite=FenetreInputNombreTournees(nomNouveauSite,nombreNouvellesEquipes,nombreNouvellesTournees)
        self.fenetreConfig2NouveauSite.confirmButton.bind("<Button-1>",self.confirmNewSiteStep2)
        self.fenetreNouveauSite.master.destroy()

    def confirmNewSiteStep2(self,event):
        nomSite=self.fenetreConfig2NouveauSite.nomSite
        nombreEquipes=self.fenetreConfig2NouveauSite.nombreEquipes
        nombreTotalTournees=self.fenetreConfig2NouveauSite.nombreTotalTournees
        nombreTourneesParEquipe=list()
        ind=0
        while ind<len(self.fenetreConfig2NouveauSite.spinboxTournees):
            valeur=int(self.fenetreConfig2NouveauSite.spinboxTournees[ind].get())
            nombreTourneesParEquipe.append(valeur)
            ind=ind+1
        self.fenetreConfig3NouveauSite=FenetreInputNomsTournees(nomSite,nombreEquipes,nombreTotalTournees,nombreTourneesParEquipe)
        self.fenetreConfig3NouveauSite.confirmButton.bind("<Button-1>",self.confirmNewSiteStep3)
        self.fenetreConfig2NouveauSite.master.destroy()

    def confirmNewSiteStep3(self,event):
        nomsToutesTournees=list()

        i=0
        nomSite=self.fenetreConfig3NouveauSite.nomSite
        nombreTotalTournees=self.fenetreConfig3NouveauSite.nombreTotalTournees

        while i < len(self.fenetreConfig3NouveauSite.nomsTourneesEquipes):
            j=0
            nomsTournees=list()
            while j < len(self.fenetreConfig3NouveauSite.nomsTourneesEquipes[i]):
                unNom=str(self.fenetreConfig3NouveauSite.nomsTourneesEquipes[i][j].get())
                nomsTournees.append(unNom)
                j=j+1
            nomsToutesTournees.append(nomsTournees)
            i=i+1
        try:
            self.model.ajoutSite(nomSite,nombreTotalTournees,nomsToutesTournees)
            self.fenetreConfig3NouveauSite.master.destroy()
            FenetrePrincipale.callback(4)
        except Exception:
            self.fenetreConfig3NouveauSite.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()

    def confirmAddTeamStep1(self):
        listeSites=self.vue.listeSites
        self.fenetreConfig1ModifySite=FenetreModifySite(listeSites)
        self.fenetreConfig1ModifySite.bouton.bind("<Button-1>",self.confirmAddTeamStep2)

    def confirmAddTourneeStep1(self):
        listeSites=self.vue.listeSites
        self.fenetreConfigAddTournee=FenetreAddTournee(listeSites)
        self.fenetreConfigAddTournee.bouton.bind("<Button-1>",self.confirmAddTourneeStep2)

    def confirmAddTourneeStep2(self,event):

        nomSite=str(self.fenetreConfigAddTournee.listeSites.get())
        numeroEquipe=self.fenetreConfigAddTournee.sbNumeroTeam.get()
        nomTournee=str(self.fenetreConfigAddTournee.inputBox.get())

        try:
            self.model.ajoutTournee(nomSite,numeroEquipe,nomTournee)
            self.fenetreConfigAddTournee.master.destroy()
            FenetrePrincipale.callback(4)
        except Exception:
            self.fenetreConfigAddTournee.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()

    def confirmDeleteTourneeStep1(self):
        listeSites=self.vue.listeSites
        self.fenetreConfigDeleteTournee=FenetreEraseTournee(listeSites)
        self.fenetreConfigDeleteTournee.bouton.bind("<Button-1>",self.confirmDeleteTourneeStep2)

    def confirmDeleteTourneeStep2(self,event):
        nomSite=str(self.fenetreConfigDeleteTournee.listeSites.get())
        numeroEquipe=self.fenetreConfigDeleteTournee.sbNumeroTeam.get()
        nomTournee=str(self.fenetreConfigDeleteTournee.inputBox.get())
        try:
            self.model.supprimerTournee(nomSite,numeroEquipe,nomTournee)
            self.fenetreConfigDeleteTournee.master.destroy()
            FenetrePrincipale.callback(4)
        except Exception:
            self.fenetreConfigDeleteTournee.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()


    def confirmModifyTourneesStep1(self):
        listeSites=self.vue.listeSites
        self.fenetreConfigModifyTournees=FenetreModifyTournees(listeSites)
        self.fenetreConfigModifyTournees.bouton.bind("<Button-1>",self.confirmModifyTourneesStep2)

    def confirmModifyTourneesStep2(self,event):
        nomSite=str(self.fenetreConfigModifyTournees.listeSites.get())
        nombreTournees=self.fenetreConfigModifyTournees.sbNumberTournee.get()
        try:
            self.model.modifierNbTournee(nomSite,nombreTournees)
            self.fenetreConfigModifyTournees.master.destroy()
            FenetrePrincipale.callback(4)
        except Exception:
            self.fenetreConfigModifyTournees.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()

    def confirmSuppressTeamStep1(self):
        listeSites=self.vue.listeSites
        self.fenetreConfigSuppressTeam=FenetreEraseTeam(listeSites)
        self.fenetreConfigSuppressTeam.bouton.bind("<Button-1>",self.confirmSuppressTeamStep2)

    def confirmSuppressTeamStep2(self,event):
        try:
            self.model.supprimerEquipe(str(self.fenetreConfigSuppressTeam.listeSites.get()),self.fenetreConfigSuppressTeam.sbNumeroTeam.get())
            self.fenetreConfigSuppressTeam.master.destroy()
            FenetrePrincipale.callback(4)
        except Exception:
            self.fenetreConfigSuppressTeam.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()

    def confirmAddTeamStep2(self,event):
        self.fenetreConfig2ModifySite=FenetreModifySite2(self.fenetreConfig1ModifySite.listeSites.get(),self.fenetreConfig1ModifySite.sbNbEquipe.get())
        self.fenetreConfig2ModifySite.confirmButton.bind("<Button-1>",self.confirmAddTeamStep3)
        self.fenetreConfig1ModifySite.master.destroy()

    def confirmAddTeamStep3(self,event):
        nomSite=self.fenetreConfig2ModifySite.nomSite
        nombreEquipes=self.fenetreConfig2ModifySite.nombreEquipes
        valeursSpinbox=list()
        i=0
        while i<len(self.fenetreConfig2ModifySite.spinboxTournees):
            valeur=int(self.fenetreConfig2ModifySite.spinboxTournees[i].get())
            valeursSpinbox.append(valeur)
            i=i+1
        self.fenetreConfig3ModifySite=FenetreInputNomsTournees(nomSite,nombreEquipes,0,valeursSpinbox)


        self.fenetreConfig3ModifySite.confirmButton.bind("<Button-1>",self.confirmAddTeamStep4)
        self.fenetreConfig2ModifySite.master.destroy()
    def confirmAddTeamStep4(self,event):
        nomsToutesTournees=list()

        i=0
        nomSite=self.fenetreConfig3ModifySite.nomSite

        while i < len(self.fenetreConfig3ModifySite.nomsTourneesEquipes):
            j=0
            nomsTournees=list()
            while j < len(self.fenetreConfig3ModifySite.nomsTourneesEquipes[i]):
                unNom=str(self.fenetreConfig3ModifySite.nomsTourneesEquipes[i][j].get())
                nomsTournees.append(unNom)
                j=j+1
            nomsToutesTournees.append(nomsTournees)
            i=i+1
        try:
            self.model.ajoutEquipe(nomSite,nomsToutesTournees)
            self.fenetreConfig3ModifySite.master.destroy()
            FenetrePrincipale.callback(4)
        except Exception:
            self.fenetreConfig3ModifySite.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()





    def openChoices(self,event):
        periodeChoisie=str(self.vue.listePeriods.get())
        periodeMinMax=self.model.definePeriodsLimits(str(self.vue.listeCSV.get()), periodeChoisie)

        self.fenetreChoix=FenetreInput(self.vue,periodeChoisie,self, periodeMinMax)
        self.fenetreChoix.bouton.bind("<Button-1>",self.beginExtraction)

    def openChoicesRecla(self,event):
        periodeChoisie=str(self.vue.listePeriods.get())
        periodeMinMax=self.model.definePeriodsLimits(str(self.vue.listeCSV.get()), periodeChoisie)
        self.fenetreChoix=FenetreInput(self.vue,periodeChoisie,self, periodeMinMax)
        self.fenetreChoix.bouton.bind("<Button-1>",self.beginReclamation)



    def beginExtraction(self,event):
        i=0
        listSites=list()
        #Là on est capable de voir la liste des boutons cochés  et de récupérer les sites sélectionnés
        while (i<len(self.vue.listVariableCheckButton)):
            if self.vue.listVariableCheckButton[i].get()==True:
                listSites.append(self.vue.listTextCheckButton[i])
            i=i+1
        if str(self.vue.listePeriods.get())=="Semaines":
            a=str(self.fenetreChoix.sbSemaines1.get())
            b=str(self.fenetreChoix.sbSemaines2.get())
            periodeEntree=a+'-'+b
        if str(self.vue.listePeriods.get())=="Mois":
            periodeEntree=str(self.fenetreChoix.sbMois.get())
        if str(self.vue.listePeriods.get())=="Trimestre":
            periodeEntree=str(self.fenetreChoix.sbTrim.get())

        try:

            self.model.readCSV1(str(self.vue.listeCSV.get()),listSites,str(self.vue.listePeriods.get()),periodeEntree)
            self.fenetreChoix.master.destroy()
            FenetrePrincipale.callback(1)
            self.vue.callbackBis(2)

        except Exception:
            self.fenetreChoix.master.destroy()
            FenetrePrincipale.callback(6)
        finally:
            self.vue.fenetre.destroy()
            self.newController=Controller()
            self.newController.run()

    def beginReclamation(self,event):

        i=0
        listSites=list()
        #Là on est capable de voir la liste des boutons cochés  et de récupérer les sites sélectionnés
        while (i<len(self.vue.listVariableCheckButton)):
            if self.vue.listVariableCheckButton[i].get()==True:
                listSites.append(self.vue.listTextCheckButton[i])
            i=i+1
        if str(self.vue.listePeriods.get())=="Semaines":
            a=str(self.fenetreChoix.sbSemaines1.get())
            b=str(self.fenetreChoix.sbSemaines2.get())
            periodeEntree=a+'-'+b
        if str(self.vue.listePeriods.get())=="Mois":
            periodeEntree=str(self.fenetreChoix.sbMois.get())
        if str(self.vue.listePeriods.get())=="Trimestre":
            periodeEntree=str(self.fenetreChoix.sbMois.get())


        self.model.readCSV2(str(self.vue.listeCSV.get()),listSites,str(self.vue.listePeriods.get()),periodeEntree)
        self.fenetreChoix.master.destroy()
        FenetrePrincipale.callback(1)
            #except Exception:
        #self.fenetreChoix.master.destroy()
        #FenetrePrincipale.callback(6)
        #finally :
        self.vue.fenetre.destroy()
        self.newController=Controller()
        self.newController.run()

    def savePDF(self):
        try:
            self.model.fromPNGToPDF("Résumé",self.model.listeImagesDossier("Graphiques/"), "Graphiques")
            FenetrePrincipale.callback(3)
        except Exception:
            FenetrePrincipale.callback(6)
