#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import csv
from PIL import Image # Faire sudo pip install pillow pour utiliser cette librairie
from fpdf import FPDF # Faire sudo pip install fpdf pour utiliser cette librairie
from collections import Counter
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt # pour les graphes, faire sudo apt-get install python-matplotlib avant
import numpy as np
from datetime import datetime
from math import *


#sudo pip install ReportLab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# Problème d'encodage
import sys
reload(sys)
sys.setdefaultencoding('utf8')

colors2=['coral', 'lightpink', 'salmon', 'burlywood', 'indianred', 'tomato', 'lightsage', 'sandybrown', 'khaki', 'thistle', 'tan', 'darksalmon', 'lightcoral', 'lightblue', 'lightsalmon', 'rosybrown', 'lightgrey'	] # revoir pour les camemberts, pas assez visibles

colors3 = ['bluesapphire', 'lightseagreen','turquoisegreen', 'mindaro','folly','warmblack', 'caribbeangreen', 'tealdeer','arcticlime','bigdiporuby','bluejeans',
'lapislazuli','sandstorm','darkliver','red']

colors = ['blue','aqua','cornflowerblue','skyblue','darkgreen','green','chartreuse','palegreen','brown','crimson','red','tomato','orangered','orange','yellow',
'khaki','purple','violet','pink']

class Model :
	def __init__(self) :
		print("Le modèle est bien instancié")
		self.listeSitesCoches=list()
		self.l_sites=self.readSites()


	""" fonction de lecture du CSV """

	def	readDirectory(self) :
		listeFichiers=list()
		for element in os.listdir("FichiersCSV/"):
			listeFichiers.append(element)
		return listeFichiers

	def readSites(self) :
		liste_sites={}
		stream=open("liste_sites","rb")
		l_sites = csv.reader(stream)
		for row in l_sites:
			liste_sites[row[0]] = {}
			liste_sites[row[0]]['nombre_tournee'] = row[1]
			liste_sites[row[0]]['liste_equipe'] = row[2]
		for site in liste_sites:
			liste_sites[site]['liste_equipe'] = liste_sites[site]['liste_equipe'].split('_')
			for equipe in range(0,len(liste_sites[site]['liste_equipe'])):
				liste_sites[site]['liste_equipe'][equipe] = liste_sites[site]['liste_equipe'][equipe].split('-')
		stream.close()
		return liste_sites

	def definePeriodsLimits(self, nomFichier, choixPeriode):
		with open("FichiersCSV/"+nomFichier, 'rb') as csvfile:

			bdd = csv.reader(csvfile, delimiter=';')
			motif=[]
			sites = {}
			nb_recla = {}
			tournee_site_date={}
			liste_recla={}
			motif_site_date = {}
			#liste_sites = []
			selection_site = []


			#lecture de la liste des sites
			l_sites = self.readSites()
			self.l_sites=l_sites

			self.MAJListeSites(self.l_sites)
			self.selectionSites(sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, selection_site)

			# détermination des dates min et max et du nombre de semaines
			#lecture du csv : lecture des motifs, separation par site
			date_min_max = self.parcoursBDD(bdd, sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, motif)
			periodeMinMax=list()

			if choixPeriode=='Mois':
				moisMin = date_min_max['date_min'].month
				moisMax=date_min_max['date_max'].month
				periodeMinMax.append(moisMin)
				periodeMinMax.append(moisMax)
			if choixPeriode=='Semaines':
				semaineMin=date_min_max['date_min'].isocalendar()[1]
				semaineMax=date_min_max['date_max'].isocalendar()[1]
				periodeMinMax.append(semaineMin)
				periodeMinMax.append(semaineMax)
			if choixPeriode=='Trimestre':
				periodeMinMax.append(1)
				periodeMinMax.append(4)
		return periodeMinMax


	""" Fonction qui se lance pour la création des graphiques sur les indicateurs"""
	def readCSV1(self,nomFichier,listeSitesCoches,choixPeriode,valeurPeriode) :
	#nomFichier=raw_input("Veuillez entrer le nom du fichier	que vous voulez analysez (suivi de l'extension ) :")
		self.listeSitesCoches=listeSitesCoches

		with open("FichiersCSV/"+nomFichier, 'rb') as csvfile:

			bdd = csv.reader(csvfile, delimiter=';')
			motif=[]
			sites = {}
			nb_recla = {}
			tournee_site_date={}
			liste_recla={}
			motif_site_date = {}
			#liste_sites = []
			selection_site = []

			#Suppression des graphes dans le dossier
			self.removeFiles()

			#lecture de la liste des sites
			l_sites = self.readSites()
			self.l_sites=l_sites
			#self.modifierNbTournee(l_sites)
			#self.ajoutSite('test', l_sites)
			#self.ajoutEquipe(l_sites)
		#	self.ajoutTournee(l_sites)
		#	self.supprimerSite(nomFichierSupprime, l_sites)
			#self.supprimerSite('ESTREES', l_sites)
		#	self.supprimerEquipe(nomFichierSupprime,l_sites)
			#self.supprimerEquipe('compiegne',l_sites)
		#	self.supprimerTournee(nomFichierSupprime,l_sites)
			#self.supprimerTournee('compiegne',l_sites)
			self.MAJListeSites(self.l_sites)
			self.selectionSites(sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, selection_site)

			# détermination des dates min et max et du nombre de semaines
			#lecture du csv : lecture des motifs, separation par site
			date_min_max = self.parcoursBDD(bdd, sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, motif)
			mois_min = date_min_max['date_min'].month
	#		csvfile.seek(0)
			nb = self.calculNbSemaine(date_min_max['date_min'], date_min_max['date_max'])
			nb_semaine = nb['nb_semaines']
			nb_mois= nb['nb_mois']
			print(date_min_max)
			print(mois_min)
			print(nb)
			print(nb_semaine)
			print(nb_mois)
			print date_min_max['date_min'].isocalendar()[1]
			print date_min_max['date_max'].isocalendar()[1]
			# Calcul des indicateurs

			if date_min_max['date_min'].isocalendar()[1] > date_min_max['date_max'].isocalendar()[1] :
				num_semaines = []
				for j in range(date_min_max['date_min'].isocalendar()[1], date_min_max['date_max'].isocalendar()[1]+54):
					if j>53:
						num_semaines.append(j-53)
					else:
						num_semaines.append(j)
			else :
				num_semaines = range(date_min_max['date_min'].isocalendar()[1], date_min_max['date_max'].isocalendar()[1]+1)

			nb_recla_semaine = self.nbReclaSemaine(nb_recla, selection_site, date_min_max['date_min'], date_min_max['date_max'], num_semaines)

			motif_site = self.motifSitesSemaines(date_min_max['date_min'], date_min_max['date_max'], motif_site_date, num_semaines)
			motif_site_semaine = motif_site['motif_site_semaine']
			motif_site_mois = motif_site['motif_site_mois']
			motif_site_trimestre = motif_site['motif_site_trimestre']


			tournee_site = self.tourneeSitesSemaines(date_min_max['date_min'], date_min_max['date_max'],	tournee_site_date, num_semaines)
			tournee_site_semaine = tournee_site['tournee_site_semaine']
			tournee_site_mois = tournee_site['tournee_site_mois']
			tournee_site_trimestre = tournee_site['tournee_site_trimestre']

			equipe_site = self.equipeSitesSemaines(date_min_max['date_min'], date_min_max['date_max'], tournee_site_date, num_semaines)
			equipe_site_semaine = equipe_site['equipe_site_semaine']
			equipe_site_mois = equipe_site['equipe_site_mois']
			equipe_site_trimestre = equipe_site['equipe_site_trimestre']

			liste_recla_site = self.listeReclaSitesSemaines(date_min_max['date_min'], date_min_max['date_max'], liste_recla, num_semaines)
			liste_recla_site_semaine = liste_recla_site['liste_recla_site_semaine']
			liste_recla_site_mois = liste_recla_site['liste_recla_site_mois']
			liste_recla_site_trimestre = liste_recla_site['liste_recla_site_trimestre']

		#choix de la semaine
			print("LIS CE QU'IL Y A ICI JUSTE EN BAS DE CE COMMENTAIRE")
			#ici on récupère un dico faudra bien faire attention à comment le récupérer avec tes MessageBox
			num_semaine_mois_trimestre = self.choixSemaineMois(nb_semaine,choixPeriode,valeurPeriode)

			self.showMotifGraph(motif_site_semaine, motif_site_mois, motif_site_trimestre, selection_site, num_semaine_mois_trimestre)
			self.showNbReclaSemaineGraph(nb_recla_semaine['nb_recla_semaine'])
			self.showNbReclaSemaineSiteGraph(nb_recla_semaine['nb_recla_semaine_site'], nb_semaine, date_min_max['date_min'], date_min_max['date_max'], num_semaines)
			#self.showSiteGraph(sites) #voir si on le garde
			self.showMotifSiteWeekGraph(motif_site_semaine, motif_site_mois, motif_site_trimestre, selection_site, num_semaine_mois_trimestre)
			self.showTopMotifSiteGraph(motif_site_semaine, motif_site_mois, motif_site_trimestre, selection_site, num_semaine_mois_trimestre)
			self.showTourneeSiteWeekGraph(tournee_site_semaine, tournee_site_mois, tournee_site_trimestre, selection_site, num_semaine_mois_trimestre)
			self.showNbReclaTourneeSiteWeekGraph(tournee_site_semaine, selection_site, date_min_max['date_min'], date_min_max['date_max'], num_semaines)
			self.showEquipeSiteWeekGraph(equipe_site_semaine, equipe_site_mois, equipe_site_trimestre, selection_site, num_semaine_mois_trimestre)

			#self.tableau_recla(liste_recla_site_semaine, liste_recla_site_mois, liste_recla_site_trimestre, selection_site, num_semaine_mois_trimestre)

	""" Ici c''est la fonction qui se lance pour le tableau de la liste des réclamations """
	def readCSV2(self,nomFichier,listeSitesCoches,choixPeriode,valeurPeriode) :
	#nomFichier=raw_input("Veuillez entrer le nom du fichier	que vous voulez analysez (suivi de l'extension ) :")
		self.listeSitesCoches=listeSitesCoches

		with open("FichiersCSV/"+nomFichier, 'rb') as csvfile:

			bdd = csv.reader(csvfile, delimiter=';')
			motif=[]
			sites = {}
			nb_recla = {}
			tournee_site_date={}
			liste_recla={}
			motif_site_date = {}
			#liste_sites = []
			selection_site = []

			#lecture de la liste des sites
			l_sites = self.readSites()
			self.l_sites=l_sites
			self.MAJListeSites(self.l_sites)
			self.selectionSites(sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, selection_site)

			# détermination des dates min et max et du nombre de semaines
			#lecture du csv : lecture des motifs, separation par site
			date_min_max = self.parcoursBDD(bdd, sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, motif)
			print("VOICI LES DATES MINI")
			print (date_min_max)
			print("VOICI LES DATES MAXI")
			mois_min = date_min_max['date_min'].month
	#		csvfile.seek(0)
			nb = self.calculNbSemaine(date_min_max['date_min'], date_min_max['date_max'])
			nb_semaine = nb['nb_semaines']
			nb_mois= nb['nb_mois']
			# Calcul des indicateurs
			if date_min_max['date_min'].isocalendar()[1] > date_min_max['date_max'].isocalendar()[1] :
				num_semaines = []
				for j in range(date_min_max['date_min'].isocalendar()[1], date_min_max['date_max'].isocalendar()[1]+54):
					if j>53:
						num_semaines.append(j%53)
					else:
						num_semaines.append(j)
			else :
				num_semaines = range(date_min_max['date_min'].isocalendar()[1], date_min_max['date_max'].isocalendar()[1]+1)


			nb_recla_semaine = self.nbReclaSemaine(nb_recla, selection_site, date_min_max['date_min'], date_min_max['date_max'], num_semaines)

			motif_site = self.motifSitesSemaines(date_min_max['date_min'], date_min_max['date_max'], motif_site_date, num_semaines)
			motif_site_semaine = motif_site['motif_site_semaine']
			motif_site_mois = motif_site['motif_site_mois']
			motif_site_trimestre = motif_site['motif_site_trimestre']


			tournee_site = self.tourneeSitesSemaines(date_min_max['date_min'], date_min_max['date_max'],	tournee_site_date, num_semaines)
			tournee_site_semaine = tournee_site['tournee_site_semaine']
			tournee_site_mois = tournee_site['tournee_site_mois']
			tournee_site_trimestre = tournee_site['tournee_site_trimestre']

			equipe_site = self.equipeSitesSemaines(date_min_max['date_min'], date_min_max['date_max'], tournee_site_date, num_semaines)
			equipe_site_semaine = equipe_site['equipe_site_semaine']
			equipe_site_mois = equipe_site['equipe_site_mois']
			equipe_site_trimestre = equipe_site['equipe_site_trimestre']

			liste_recla_site = self.listeReclaSitesSemaines(date_min_max['date_min'], date_min_max['date_max'], liste_recla, num_semaines)
			liste_recla_site_semaine = liste_recla_site['liste_recla_site_semaine']
			liste_recla_site_mois = liste_recla_site['liste_recla_site_mois']
			liste_recla_site_trimestre = liste_recla_site['liste_recla_site_trimestre']


			#ici on récupère un dico faudra bien faire attention à comment le récupérer avec tes MessageBox
			num_semaine_mois_trimestre = self.choixSemaineMois(nb_semaine,choixPeriode,valeurPeriode)
			self.tableau_recla(liste_recla_site_semaine, liste_recla_site_mois, liste_recla_site_trimestre, selection_site, num_semaine_mois_trimestre)
	# suppression des graphes dans le dossier
	def removeFiles(self):
		path = "Graphiques"
		files=os.listdir(path)
		for x in files:
			if not x in '0pageDeGarde.png' :
				print("haha")
				os.remove(path+'/'+x)
				path = "Graphiques"


	def modifierNbTournee(self, site, nombre):
		#site = raw_input("nom du site pour lequel vous voulez modifier le nombre de tournée")
		#nombre = raw_input("nombre de tournée")
		self.l_sites[site.upper()]['nombre_tournee'] = int(nombre)
		self.MAJListeSites(self.l_sites)

	# ajout d'un site dans le fichier et dans la liste courante
	def ajoutSite(self, nomNouveauFichier,nombreTournee,nomsTournees):
		site = nomNouveauFichier
		site = site.upper()
		#nombreTournee = raw_input('Nombre de tournee \n')
		self.l_sites[site] = {}
		self.l_sites[site]['nombre_tournee'] = nombreTournee
	#	rep = raw_input('ajouter une equipe -> taper 1')
		equipes = []
		x=0


	#	while rep == '1':
		print("Voici le contenu de nomsTournees")
		print(nomsTournees)
		print("Voici la taille de nomTournees")
		print(len(nomsTournees))
		while x<len(nomsTournees):

			#rep_2 = raw_input('ajouter tournee dans lequipe -> taper 1')
			tournees = []
			y=0
			while y < len(nomsTournees[x]):
				tournee = str(nomsTournees[x][y])
				tournees.append(tournee)
				y=y+1
				#rep_2 = raw_input('ajouter tournee dans lequipe -> taper 1')
			equipes.append(tournees)
			x=x+1
			#rep = raw_input('ajouter une equipe -> taper 1')
		print("Voici la variable equipes")
		print(equipes)
		self.l_sites[site]['liste_equipe'] = equipes
		print "Voici l_sites"
		print(self.l_sites)
		self.MAJListeSites(self.l_sites)

	def ajoutEquipe(self, nomSite,nomsTournees):
		site = nomSite
		#rep = raw_input('ajouter une equipe -> taper 1\n')
		equipes = []
		x=0
		while x<len(nomsTournees):
			#rep_2 = raw_input('ajouter tournee dans lequipe -> taper 1\n')
			y=0
			tournees = []
			while y<len(nomsTournees[x]):
				tournee = nomsTournees[x][y]
				tournee=tournee.upper()
				tournees.append(tournee)
				y=y+1
				#rep_2 = raw_input('ajouter tournee dans lequipe -> taper 1\n')
			x=x+1
			self.l_sites[site]['liste_equipe'].append(tournees)
			#rep = raw_input('ajouter une equipe -> taper 1')
		#if raw_input('Voulez-vous modifier le nombre de tournée? taper 1\n')=='1':
			#self.modifierNbTournee(l_sites)
			self.MAJListeSites(self.l_sites)


	def ajoutTournee(self,site, numEquipe, tournee):
	#	site = raw_input('nom du site auquel vous voulez ajouter une tournee')
	#	numEquipe = raw_input('Numero de lequipe:\n')
	#	rep = raw_input('ajouter tournee dans lequipe -> taper 1\n')
	#	while rep == '1':
	#	tournee = raw_input('tournee = ')
		tournee=tournee.upper()
		self.l_sites[site]['liste_equipe'][int(numEquipe)-1].append(tournee)
		#rep = raw_input('ajouter tournee dans lequipe -> taper 1\n')
		#if raw_input('Voulez-vous modifier le nombre de tournée? taper 1\n')=='1':
		#self.modifierNbTournee(l_sites)
		self.MAJListeSites(self.l_sites)
		print self.l_sites

	# suppression d'un site dans le fichier et dans la liste courante
	def supprimerSite(self,nomFichierSupprime):
		print 'SUPPRESSION SITE'
		site = nomFichierSupprime
		site = site.upper()
		self.l_sites.pop(site, None)
		self.MAJListeSites(self.l_sites)

	def supprimerEquipe(self,nomFichierSupprime, numEquipe):
		print 'SUPPRESSION EQUIPE'
		site = nomFichierSupprime
		site = site.upper()
		#numEquipe = raw_input('Numero de lequipe:\n')
		self.l_sites[site]['liste_equipe'].pop(int(numEquipe)-1)
		self.MAJListeSites(self.l_sites)


	def supprimerTournee(self,site,numEquipe,nomTournee):
		print 'SUPPRESSION TOURNEE'
		#site = nomFichierSupprime
		site = site.upper()
		nomTournee=nomTournee.upper()
		#numEquipe = raw_input('Numero de lequipe:\n')
		#nomTournee = raw_input('Nom de la tournée:\n')
		self.l_sites[site]['liste_equipe'][int(numEquipe)-1].remove(nomTournee)
		self.MAJListeSites(self.l_sites)

	def MAJListeSites(self, l_sites):
		print("On est dans MAJListeSites")
		print("Voici le contenu de l_sites")
		print(l_sites)
		fichier = open("liste_sites", "rb")
		fichier1=open("liste_sites_temp", "wb")
		c_write = csv.writer(fichier1)

		#ecriture de la nouvelle liste dans un fichier temporaire puis suppression
		for site in l_sites:
			equipes = ""
			for equipe in range(0,len(l_sites[site]['liste_equipe'])):
				tournees = str(l_sites[site]['liste_equipe'][equipe][0])
				for tournee in range(1,len(l_sites[site]['liste_equipe'][equipe])):
					tournees = tournees+'-'+l_sites[site]['liste_equipe'][equipe][tournee]
				equipes = equipes+'_'+tournees
			c_write.writerow([site,l_sites[site]['nombre_tournee'],equipes[1:]])
		os.remove("liste_sites")
		os.renames("liste_sites_temp", "liste_sites")
		fichier1.close()
		fichier.close()


	def selectionSites(self, sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, selection_site):
		#ajout du site s'il est demandé
		print(self.listeSitesCoches)
		for site in self.listeSitesCoches:
	#		question = raw_input("Souhaitez-vous les indicateurs pour "+site+" ?")
	#		if (question== "oui" or question =="OUI" or question =="O" or question=="o" or question=="yes"):
			sites[site] = []
			tournee_site_date[site] = []
			motif_site_date[site]=[]
			nb_recla[site] = []
			liste_recla[site] = []

			selection_site.append(site)
		print(selection_site)
		print(motif_site_date)
		print(tournee_site_date)
		print(sites)

	""" Parcours du fichier BDD et récupération des infos """
	def parcoursBDD(self,bdd, sites, nb_recla, liste_recla, motif_site_date, tournee_site_date, motif):

		date_max = datetime.strptime("01/01/1900 01:01", '%d/%m/%Y %H:%M')
		date_min = datetime.strptime("12/12/2020 00:00", '%d/%m/%Y %H:%M')
		i = 0
		for row in bdd:
			if '' != row[13]: # enlever le motif vide
				i = i+1
				motif.append(row[13])
			if row[49] != 'Date de la demande':
				date = datetime.strptime(row[49], '%d/%m/%Y %H:%M')
				# Détermination de la date max et de la date min
				if date_max < date :
					date_max = date
				if date_min > date:
					date_min = date
				# Séparation des reclamations par site et ajout de la date
				for site in sites:
					if str(site) in row[46]:
						nb_recla[site].append(date.isocalendar()[1])
						if '' != row[13]:
							sites[site].append(row[13])
							motif_site_date[site].append([row[13], date])
						if '' != row[47]:
							tournee_site_date[site].append([row[47], date])
						liste_recla[site].append([row[1]+' '+row[51]+' '+row[52], row[4]+' '+row[5]+' '+row[8]+' '+row[9], date, row[47], row[13], row[28]])
		return {'date_min':date_min, 'date_max':date_max}

	""" Détermination de la semaine du motif et par site """
	def calculNbSemaine(self,date_min, date_max):
		diff = date_max - date_min
		nb_jours = diff.days
		nb_semaines = int(ceil(nb_jours/7.0)) # arrondi supérieur
		nb_mois = date_max.month - date_min.month + 1
		print nb_semaines
		print nb_mois
		return {'nb_semaines':nb_semaines, 'nb_mois': nb_mois}



		# à modifier on compte le nombre de réclamations pas le nombre de semaine
	def nbReclaSemaine(self, nb_recla, selection_site, date_min, date_max, num_semaines):
		nb_recla_semaine = {}
		nb_recla_semaine_site = {}
		for i in num_semaines:
			nb_recla_semaine['semaine '+str(i)] = 0
		print nb_recla_semaine
		for site in selection_site:
			nb_recla_semaine_site[site] = {}
			nombre_reclamation = Counter(nb_recla[site])
			for semaine in num_semaines:
				nb_recla_semaine['semaine '+str(semaine)] = nb_recla_semaine['semaine '+str(semaine)] + nombre_reclamation[semaine]
				if nombre_reclamation[semaine]:
					nb_recla_semaine_site[site]['semaine '+str(semaine)] = nombre_reclamation[semaine]
				else:
					nb_recla_semaine_site[site]['semaine '+str(semaine)] = 0
		print nb_recla_semaine
		print nb_recla_semaine_site
		return {'nb_recla_semaine': nb_recla_semaine, 'nb_recla_semaine_site':nb_recla_semaine_site}

	def tourneeSitesSemaines(self, date_min, date_max, tournee_site_date, num_semaines):
		tournee_site_semaine = {}
		tournee_site_mois = {}
		tournee_site_trimestre = {}
		for i in num_semaines:
			tournee_lieu = {}
			for site in tournee_site_date:
				tournee_lieu[site+str(i)] = []
				#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			tournee_site_semaine[str(i)] = tournee_lieu
		print 'tournee_site_semaine'
		print tournee_site_semaine

		for i in range(date_min.month, date_max.month+1):
			tournee_lieu = {}
			for site in tournee_site_date:
				tournee_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			tournee_site_mois[str(i)]= tournee_lieu
		print 'tournee_site_mois'
		print tournee_site_mois

		for i in range(1, 4+1):
			tournee_lieu = {}
			for site in tournee_site_date:
				tournee_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			tournee_site_trimestre[str(i)] = tournee_lieu
		print 'trimestre'
		print tournee_site_trimestre

		for rows in tournee_site_date :
			for row in tournee_site_date[rows]:
				diff_date = row[1] - date_min
				semaine = row[1].isocalendar()[1]
				tournee_site_semaine[str(semaine)][rows+str(semaine)].append(row[0])
				mois = row[1].month
				trimestre = int(ceil(mois/3.))
				tournee_site_mois[str(mois)][rows+str(mois)].append(row[0])
				tournee_site_trimestre[str(trimestre)][rows+str(trimestre)].append(row[0])
		return {'tournee_site_semaine': tournee_site_semaine, 'tournee_site_mois': tournee_site_mois, 'tournee_site_trimestre': tournee_site_trimestre}

	def equipeSitesSemaines(self, date_min, date_max, tournee_site_date, num_semaines):
		equipe_site_semaine = {}
		equipe_site_mois = {}
		equipe_site_trimestre = {}
		for i in num_semaines:
			equipe_lieu = {}
			for site in tournee_site_date:
				equipe_lieu[site+str(i)] = []
				#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			equipe_site_semaine[str(i)] = equipe_lieu
		print 'equipe_site_semaine'
		print equipe_site_semaine

		for i in range(date_min.month, date_max.month+1):
			equipe_lieu = {}
			for site in tournee_site_date:
				equipe_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			equipe_site_mois[str(i)]= equipe_lieu
		print 'equipe_site_mois'
		print equipe_site_mois

		for i in range(1, 4+1):
			equipe_lieu = {}
			for site in tournee_site_date:
				equipe_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			equipe_site_trimestre[str(i)] = equipe_lieu
		print 'equipe_site_trimestre'
		print equipe_site_trimestre

		for rows in tournee_site_date :
			for row in tournee_site_date[rows]:
				diff_date = row[1] - date_min
				semaine = row[1].isocalendar()[1]
				mois = row[1].month
				trimestre = int(ceil(mois/3.))
				equipe_site_semaine[str(semaine)][rows+str(semaine)] = {}
				equipe_site_mois[str(mois)][rows+str(mois)] = {}
				equipe_site_trimestre[str(trimestre)][rows+str(trimestre)] = {}
				for i in range(0, len(self.l_sites[rows]['liste_equipe'])):
					equipe_site_semaine[str(semaine)][rows+str(semaine)]['Equipe '+str(i+1)] = []
					equipe_site_mois[str(mois)][rows+str(mois)]['Equipe '+str(i+1)] = []
					equipe_site_trimestre[str(trimestre)][rows+str(trimestre)]['Equipe '+str(i+1)] = []
					r = re.compile(".*"+str(row[0]))
					if filter(r.match, self.l_sites[rows]['liste_equipe'][i]):
						equipe_site_semaine[str(semaine)][rows+str(semaine)]['Equipe '+str(i+1)].append(filter(r.match, self.l_sites[rows]['liste_equipe'][i])[0])
						equipe_site_mois[str(mois)][rows+str(mois)]['Equipe '+str(i+1)].append(filter(r.match, self.l_sites[rows]['liste_equipe'][i])[0])
						equipe_site_trimestre[str(trimestre)][rows+str(trimestre)]['Equipe '+str(i+1)].append(filter(r.match, self.l_sites[rows]['liste_equipe'][i])[0])
		print 'equipe_site_semaine'
		print equipe_site_semaine
		print 'equipe_site_mois'
		print equipe_site_mois
		print 'equipe_site_trimestre'
		print equipe_site_trimestre
		return {'equipe_site_semaine': equipe_site_semaine, 'equipe_site_mois': equipe_site_mois, 'equipe_site_trimestre': equipe_site_trimestre}

	def motifSitesSemaines(self, date_min, date_max, motif_site_date, num_semaines):
		motif_site_semaine = {}
		motif_site_mois = {}
		motif_site_trimestre = {}

		print num_semaines
		for i in num_semaines:
			motif_lieu = {}
			for site in motif_site_date:
				motif_lieu[site+str(i)] = []
				#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			motif_site_semaine[str(i)] = motif_lieu
		print motif_site_semaine


		for i in range(date_min.month, date_max.month+1):
			motif_lieu = {}
			print i
			for site in motif_site_date:
				motif_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			motif_site_mois[str(i)]= motif_lieu


		for i in range(1, 4+1):
			motif_lieu = {}
			for site in motif_site_date:
				motif_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			motif_site_trimestre[str(i)] = motif_lieu


		for rows in motif_site_date :
			for row in motif_site_date[rows]:
				diff_date = row[1] - date_min
				semaine = row[1].isocalendar()[1]
				motif_site_semaine[str(semaine)][rows+str(semaine)].append(row[0])
				mois = row[1].month
				trimestre = int(ceil(mois/3.))
				motif_site_mois[str(mois)][rows+str(mois)].append(row[0])
				motif_site_trimestre[str(trimestre)][rows+str(trimestre)].append(row[0])

		print 'motif_site_semaine'
		print motif_site_semaine
		print 'motif_site_mois'
		print motif_site_mois
		print 'motif_site_trimestre'
		print motif_site_trimestre

		return {'motif_site_semaine': motif_site_semaine, 'motif_site_mois': motif_site_mois, 'motif_site_trimestre': motif_site_trimestre}

	def listeReclaSitesSemaines(self, date_min, date_max, liste_recla, num_semaines):
		liste_recla_site_semaine = {}
		liste_recla_site_mois = {}
		liste_recla_site_trimestre = {}
		for i in num_semaines:
			recla_lieu = {}
			for site in liste_recla:
				recla_lieu[site+str(i)] = []
				#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			liste_recla_site_semaine[str(i)] = recla_lieu


		for i in range(date_min.month, date_max.month+1):
			recla_lieu = {}
			for site in liste_recla:
				recla_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			liste_recla_site_mois[str(i)]= recla_lieu


		for i in range(1, 4+1):
			recla_lieu = {}
			for site in liste_recla:
				recla_lieu[site+str(i)] = []
		#besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
			liste_recla_site_trimestre[str(i)] = recla_lieu


		for rows in liste_recla :
			for row in liste_recla[rows]:
				diff_date = row[2] - date_min
				semaine = row[2].isocalendar()[1]
				mois = row[2].month
				row[2] = row[2].strftime('%d/%m/%Y %H:%M')
				liste_recla_site_semaine[str(semaine)][rows+str(semaine)].append(row)

				trimestre = int(ceil(mois/3.))
				liste_recla_site_mois[str(mois)][rows+str(mois)].append(row)
				liste_recla_site_trimestre[str(trimestre)][rows+str(trimestre)].append(row)

		print 'liste_recla_site_semaine'
		print liste_recla_site_semaine
		print 'liste_recla_site_mois'
		print liste_recla_site_mois
		print 'liste_recla_site_trimestre'
		print liste_recla_site_trimestre

		return {'liste_recla_site_semaine': liste_recla_site_semaine, 'liste_recla_site_mois' : liste_recla_site_mois, 'liste_recla_site_trimestre' : liste_recla_site_trimestre}



	def choixSemaineMois(self,nb_semaine,choixPeriode,valeurPeriode):
		intervalle = choixPeriode
		num = {}
		if intervalle == 'Semaines':
			num['semaine'] = valeurPeriode
			if re.search('d*-d*', num['semaine']):
				print num['semaine']
				num['semaine'] = num['semaine'].split("-")
		elif intervalle == 'Mois':
			num['mois'] = valeurPeriode
		elif intervalle == 'Trimestre':
			num['trimestre'] = valeurPeriode
		return num


	 #Calcul du nombre de réclamations par motif pour tous les sites selctionnés
	def showMotifGraph (self, motif_site_semaine, motif_site_mois, motif_site_trimestre, selection_site, num_semaine_mois_trimestre):
		print("HAHAHAHAH On est dans le code de Show Motif graph motherfucker")

		# Calcul du nombre de reclamation par motifs
		# Construction du camembert
		motifs = []
		plt.figure(figsize=(12,10))
		if num_semaine_mois_trimestre.keys()[0] == 'semaine':
			if type(num_semaine_mois_trimestre.values()[0]) == type(list()):
				if int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1]):
					num_semaines = []
					for j in range(int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1])+53):
						if j>53:
							num_semaines.append(j%53)
						else:
							num_semaines.append(j)
				else :
					num_semaines = range(int(num_semaine_mois_trimestre.values()[0][0]),int(num_semaine_mois_trimestre.values()[0][1])+1)
				for i in num_semaines:
					for site in selection_site:
						for motif in motif_site_semaine[str(i)][site+str(i)]:
							motifs.append(motif)
				nb_motifs = Counter(motifs)
				name = nb_motifs.keys()
				data = nb_motifs.values()
				plt.title('Nombre de réclamations par motifs pour l\'ensemble des sites\n pour les semaines '+num_semaine_mois_trimestre.values()[0][0]+' à '+num_semaine_mois_trimestre.values()[0][1], fontsize=16)

			else:
				for site in selection_site:
					if motif_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]:
						for motif in motif_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]:
							motifs.append(motif)
				nb_motifs = Counter(motifs)
				name = nb_motifs.keys()
				data = nb_motifs.values()
				plt.title('Nombre de réclamations par motifs l\'ensemble des sites \n pour la semaine '+num_semaine_mois_trimestre['semaine'], fontsize=16)
		#mois
		elif num_semaine_mois_trimestre.keys()[0] == 'mois':
			for site in selection_site:
				if motif_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
					for motif in motif_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
						motifs.append(motif)
			nb_motifs = Counter(motifs)
			name = nb_motifs.keys()
			data = nb_motifs.values()
			plt.title('Nombre de réclamations par motifs \n pour l\'ensemble des sites pour le mois '+num_semaine_mois_trimestre['mois'], fontsize=16)
		#trimestre
		elif num_semaine_mois_trimestre.keys()[0] == 'trimestre':
			for site in motif_site_trimestre[num_semaine_mois_trimestre['trimestre']]:
				if motif_site_trimestre[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
					for motif in motif_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']]:
						motifs.append(motif)
			nb_motifs = Counter(motifs)
			name = nb_motifs.keys()
			data = nb_motifs.values()
			plt.title('Nombre de réclamations par motifs \n pour '+site+' pour l\'ensemble des sites pour le trimestre '+num_semaine_mois_trimestre['trimestre'], fontsize=16)

		explode= np.zeros(len(nb_motifs))

		plt.pie(data, explode=explode, autopct = lambda x: str(round(x, 1)) + '%', shadow=False, colors=colors)
		#plt.axis('equal')

		plt.legend(name,prop={'size':11},bbox_to_anchor=(1.14,0.16), ncol=2)
		plt.savefig('Graphiques/1-' + 'nb_recla_motifs.png', dpi=120)
		plt.close()
		print("On est à la fin de showmotifgraph juste après le close")


	# Calcul du nombre de reclamation pour tous les sites séléctionnés par semaine
	def showNbReclaSemaineGraph(self,nb_recla_semaine):
		print 'SHOW NB RECLA SEMAINE'
		print nb_recla_semaine
		nb_recla_semaine=sorted(nb_recla_semaine.items(),key=lambda t : t[0])
		fig = plt.figure(figsize=(12,10))
		ax = fig.add_subplot(111)
		# Construction du graphe
		fig = plt.figure(figsize=(12,10))
		labels = []
		values = []
		for element in nb_recla_semaine:
			labels.append(element[0])
			values.append(element[1])
		indexes = np.arange(len(labels))
		width = 1
		if values :
			plt.bar(indexes, values, width, color=colors)
			plt.xticks(indexes + width * 0.5, labels)
			#plt.axis('equal')
			ax.set_ylim(0, max(values))
			plt.xlabel('Semaines du fichier')
			plt.ylabel('Nombre de réclamations')
			plt.title('Nombre de réclamations par semaine',fontsize=16)
			plt.savefig('Graphiques/' + '2-nb_recla_semaine.png', fontsize='20', dpi=120)
		#plt.show()
		plt.close()


		# Calcul du nombre de reclamation par site pour chaque semaine du fichier
		# ok mais voir pour bien séparer les barres pour chaque semaine
		# ajouter le total par site
	def showNbReclaSemaineSiteGraph(self, nb_recla_semaine_site, nb_semaine, date_min, date_max, num_semaines):
		print 'SHOW NB RECLA SEMAINE SITE'
		print nb_recla_semaine_site
		fig = plt.figure(figsize=(12,10))
		ax = fig.add_subplot(111)
		ind = np.arange(len(num_semaines))
		width = 0.10
		labels = []
		i = 0
		for site in nb_recla_semaine_site:
			labels.append(site)
			print site
			print nb_recla_semaine_site[site]
			nb_recla_semaine_site[site]=sorted(nb_recla_semaine_site[site].items(), key=lambda t : t[0])
			xTickMarks = []
			values = []

			for element in nb_recla_semaine_site[site]:
				values.append(element[1])
				xTickMarks.append(element[0])
			print values
			print ind
			ind = ind+width
			if values :
				ax.bar(ind, values, width, color=colors[i])
			i = i + 1


		# Construction du graphe
		ax.legend(labels, prop={'size':12})
		#xTickMarks = ['Semaine '+str(i) for i in num_semaines]
		#print xTickMarks
		ax.set_xticks(ind)
		xtickNames = ax.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=20, fontsize=12)
		plt.title('Nombre de réclamations par site pour chaque semaine',fontsize=16)
		plt.xlabel('Semaines du fichier')
		plt.ylabel('Nombre de réclamations')
		plt.savefig('Graphiques/' + '3-nb_recla_semaine_site.png', fontsize='20', dpi=120)
		#plt.show()
		plt.close()


		# Calcul du nombre de réclamations par site pour une semaine et affichage des graphes pour chaque site dans un png
	def showMotifSiteWeekGraph(self, motif_site_semaine, motif_site_mois, motif_site_trimestre, selection_site, num_semaine_mois_trimestre):
		for site in selection_site:
			plt.figure(figsize=(12,10))
			#semaines
			if num_semaine_mois_trimestre.keys()[0] == 'semaine':
				if type(num_semaine_mois_trimestre.values()[0]) == type(list()):
					semaines = {}
					semaines[site] = []
					if int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1]):
						num_semaines = []
						for j in range(int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1])+53):
							if j>53:
								num_semaines.append(j%53)
							else:
								num_semaines.append(j)
					else :
						num_semaines = range(int(num_semaine_mois_trimestre.values()[0][0]),int(num_semaine_mois_trimestre.values()[0][1])+1)
					for i in num_semaines:
						for motif in motif_site_semaine[str(i)][site+str(i)]:
							semaines[site].append(motif)
					count = Counter(semaines[site])
					name = count.keys()
					data = count.values()
					plt.title('Nombre de réclamations par motifs \n pour '+site+' pour les semaines '+num_semaine_mois_trimestre.values()[0][0]+' à '+num_semaine_mois_trimestre.values()[0][1], fontsize=16)

				elif motif_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]:
						count = Counter(motif_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']])
						name = count.keys()
						data = count.values()
						plt.title('Nombre de réclamations par motifs \n pour '+site+' pour la semaine '+num_semaine_mois_trimestre['semaine'], fontsize=16)
			#mois
			elif num_semaine_mois_trimestre.keys()[0] == 'mois':
				if motif_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
						count = Counter(motif_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']])
						name = count.keys()
						data = count.values()
						plt.title('Nombre de réclamations par motifs \n pour '+site+' pour le mois '+num_semaine_mois_trimestre['mois'], fontsize=16)
			#trimestre
			elif num_semaine_mois_trimestre.keys()[0] == 'trimestre':
				count = Counter(motif_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']])
				name = count.keys()
				data = count.values()
				plt.title('Nombre de réclamations par motifs \n pour '+site+' pour le trimestre '+num_semaine_mois_trimestre['trimestre'], fontsize=16)


			# Construction du camembert
			if data :
				explode = np.zeros(len(data))
				plt.pie(data, explode=explode, autopct = lambda x: str(round(x, 1)) + '%', shadow=False, colors=colors)
				plt.legend(name,bbox_to_anchor=(1.13,0.10),prop={'size':11}, ncol=2)
				plt.savefig('Graphiques/4-motif-'+site+'-'+num_semaine_mois_trimestre.keys()[0]+'.png')
			plt.close()


	def showTourneeSiteWeekGraph(self,tournee_site_semaine, tournee_site_mois, tournee_site_trimestre, selection_site, num_semaine_mois_trimestre):
		print 'SHOW TOURNEE SITE WEEK'
		for site in selection_site:
			fig = plt.figure(figsize=(15,12))
			ax = fig.add_subplot(111)
			#semaines
			if num_semaine_mois_trimestre.keys()[0] == 'semaine':
				if type(num_semaine_mois_trimestre.values()[0]) == type(list()):
					semaines = {}
					semaines[site] = []
					if int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1]):
						num_semaines = []
						for j in range(int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1])+53):
							if j>53:
								num_semaines.append(j%53)
							else:
								num_semaines.append(j)
					else :
						num_semaines = range(int(num_semaine_mois_trimestre.values()[0][0]),int(num_semaine_mois_trimestre.values()[0][1])+1)
					for i in num_semaines:
						print i
						for tournee in tournee_site_semaine[str(i)][site+str(i)]:
							semaines[site].append(tournee)
					count = Counter(semaines[site])
					name = count.keys()
					data = count.values()
					plt.title('Nombre de réclamations par tournee \n pour '+site+' pour les semaines '+num_semaine_mois_trimestre.values()[0][0]+' à '+ num_semaine_mois_trimestre.values()[0][1], fontsize=16)
				elif tournee_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]:
						count = Counter(tournee_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']])
						name = count.keys()
						data = count.values()
						plt.title('Nombre de réclamations par tournee \n pour '+site+' pour la semaine '+num_semaine_mois_trimestre['semaine'], fontsize=16)
			#mois
			elif num_semaine_mois_trimestre.keys()[0] == 'mois':
				if tournee_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
					count = Counter(tournee_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']])
					name = count.keys()
					data = count.values()
					plt.title('Nombre de réclamations par tournee \n pour '+site+' pour le mois '+num_semaine_mois_trimestre['mois'], fontsize=16)
			#trimesre
			elif num_semaine_mois_trimestre.keys()[0] == 'trimestre':
					if tournee_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']]:
						count = Counter(tournee_site_mois[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']])
						name = count.keys()
						data = count.values()
						plt.title('Nombre de réclamations par tournee \n pour '+site+' pour le trimestre '+num_semaine_mois_trimestre['trimestre'], fontsize=16)


			# Construction du graphe
			if data :
				labels = name
				values = data
				indexes = np.arange(len(labels))
				width = 1
				plt.xlabel('Nom des tournées')
				plt.ylabel('Nombre de réclamations')
				ax.set_ylim(0,max(values)+0.4*max(values))
				plt.bar(indexes, values, width, color=colors)
				plt.xticks(indexes+width*0.5, labels, rotation=45)
				plt.savefig('Graphiques/5-tournee-'+site+'-'+num_semaine_mois_trimestre.keys()[0]+'.png')
			plt.close()


	def showNbReclaTourneeSiteWeekGraph(self,tournee_site_semaine, selection_site, date_min, date_max, num_semaines):
		print 'SHOW NB RECLA PAR TOURNEE SITE WEEK'
		nb_semaines = len(num_semaines)
		plt.figure(figsize=(12,10))
		#ax = fig.add_subplot(111)
		ind = np.arange(len(num_semaines))
		width = 0.10
		labels = []
		i = 0
		max_value = -1.0

		for site in selection_site:
			values = []
			x = []
			sticks = []
			labels.append(site)
			for semaine in num_semaines:
				x.append(int(semaine))
				sticks.append('Semaine '+str(semaine))
				res =	float(len(tournee_site_semaine[str(semaine)][site+str(semaine)]))/float(self.l_sites[site]['nombre_tournee'])
				values.append(round(res,2))
				if max(values) > max_value:
					max_value = max(values)
			plt.plot(x, values, color=colors[i], linestyle='-')
			i = i + 1
		print x
		print sticks

		# Construction du camembert
		plt.legend(labels, prop={'size':12})
		#ax.set_ylim(0,max_value+0.4*max_value)
		#plt.axis([0, nb_semaines, 0, max_value+0.4*max_value])
		plt.xticks(x, sticks, rotation = 20)
		#plt.xlabel('Numéro de la semaine')
		plt.xlabel('Semaines')
		plt.ylabel('Nombre de réclamations/Nombre de tournées')
		plt.title('Ratio du nombre de réclamation pour une \n tournée pour chaque semaine', fontsize=16)
		plt.savefig('Graphiques/6-nbReclaTournee-'+site+'.png', dpi=120)
		plt.close()


	""" Calcul du nombre de réclamations par site et affichage des graphes pour chaque site dans un png -> on garde ??? pour toutes les semaines du fichier, pas interessant
	def showSiteGraph(self,sites) :
		print("HAHAHAH on est dans le code de ShowShiteGraph")
		for site in sites:
			count_sites = Counter(sites[site])
			name = count_sites.keys()
			data = count_sites.values()
			# Construction du camembert
			explode = np.zeros(len(count_sites))
			plt.figure(figsize=(12,10))
			plt.pie(data, explode=explode, autopct = lambda x: str(round(x, 1)) + '%',shadow=False, colors=colors)
			 #plt.axis('equal')
			plt.title('Nombre de réclamations par motifs pour '+site)
			plt.legend(name,bbox_to_anchor=(1.13,0.20), prop={'size':9})
			plt.savefig('Graphiques/3-'+site+'.png', fontsize='20', dpi=170)
			plt.close()
"""

#a finir

	def showEquipeSiteWeekGraph(self, equipe_site_semaine, equipe_site_mois, equipe_site_trimestre, selection_site, num_semaine_mois_trimestre):
		print 'SHOW EQUIPE SITE WEEK'

		for site in selection_site:
			print site
			fig = plt.figure(figsize=(12,10))
			ax = fig.add_subplot(111)
			labels = []
			values = []
			if num_semaine_mois_trimestre.keys()[0] == 'semaine':
				if type(num_semaine_mois_trimestre.values()[0]) == type(list()):
					semaines = {}
					semaines[site] = []
					l = []
					if int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1]):
						num_semaines = []
						for j in range(int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1])+53):
							if j>53:
								num_semaines.append(j%53)
							else:
								num_semaines.append(j)
					else :
						num_semaines = range(int(num_semaine_mois_trimestre.values()[0][0]),int(num_semaine_mois_trimestre.values()[0][1])+1)
					for i in num_semaines:
						for equipe in equipe_site_semaine[str(i)][site+str(i)]:
							for n in range(0,len(equipe_site_semaine[str(i)][site+str(i)][equipe])):
								l.append(equipe)
					count = Counter(l)
					labels = count.keys()
					values = count.values()

					plt.title('Nombre de réclamations par equipe \n pour '+site+' pour les semaines '+num_semaine_mois_trimestre.values()[0][0]+' à '+ num_semaine_mois_trimestre.values()[0][1], fontsize=16)
				elif equipe_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]:
						for equipe in equipe_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]:
							labels.append(equipe)
							values.append(len(equipe_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']][equipe]))
						plt.title('Nombre de réclamations par équipe \n pour '+site+' pour la semaine '+num_semaine_mois_trimestre['semaine'], fontsize=16)
			#mois
			elif num_semaine_mois_trimestre.keys()[0] == 'mois':
				if equipe_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
					for equipe in equipe_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
						labels.append(equipe)
						values.append(len(equipe_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']][equipe]))
					print labels
					print values
					plt.title('Nombre de réclamations par équipe \n pour '+site+' pour le mois '+num_semaine_mois_trimestre['mois'], fontsize=16)
			#trimesre
			elif num_semaine_mois_trimestre.keys()[0] == 'trimestre':
				if equipe_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']]:
					for equipe in equipe_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']]:
						labels.append(equipe)
						values.append(len(equipe_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']][equipe]))
					print labels
					print values
					plt.title('Nombre de réclamations par équipe \n pour '+site+' pour le trimestre '+num_semaine_mois_trimestre['trimestre'], fontsize=16)

			empty = 0
			for i in range(0, len(values)):
				if values[i] !=0:
					empty = 1
				# Construction du graphe
			if empty:
				indexes = np.arange(len(labels))
				width = 1
				ax.set_ylim(0,max(values)+0.4*max(values))
				plt.bar(indexes, values, width*0.5, color=colors)
				#plt.legend(labels, bbox_to_anchor=(1.13, 1), prop={'size':12})
				plt.xticks(indexes, labels, rotation=20)
				plt.xlabel('Equipe')
				plt.ylabel('Nombre de réclamations')
				plt.savefig('Graphiques/7-equipe-'+site+'-'+num_semaine_mois_trimestre.keys()[0]+'.png')
			plt.close()

	def showTopMotifSiteGraph(self, motif_site_semaine, motif_site_mois, motif_site_trimestre, selection_site, num_semaine_mois_trimestre):
		print 'SHOW TOP MOTIFS'
		for site in selection_site:
			fig = plt.figure(figsize=(12,10))
			ax = fig.add_subplot(111)
			labels = []
			values = []
			if num_semaine_mois_trimestre.keys()[0] == 'semaine':
				if type(num_semaine_mois_trimestre.values()[0]) == type(list()):
					semaines = {}
					semaines[site] = []
					if int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1]):
						num_semaines = []
						for j in range(int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1])+53):
							if j>53:
								num_semaines.append(j%53)
							else:
								num_semaines.append(j)
					else :
						num_semaines = range(int(num_semaine_mois_trimestre.values()[0][0]),int(num_semaine_mois_trimestre.values()[0][1])+1)
					for i in num_semaines:
						print i
						for motif in motif_site_semaine[str(i)][site+str(i)]:
							semaines[site].append(motif)
					count = Counter(semaines[site]).most_common(5)

					for element in count:
						labels.append(element[0])
						values.append(element[1])
					plt.title('Top des réclamations pour '+site+'\n pour les semaines '+num_semaine_mois_trimestre.values()[0][0]+' à '+ num_semaine_mois_trimestre.values()[0][1], fontsize=16)
				elif motif_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]:
						count = Counter(motif_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]).most_common(5)

						for element in count:
							labels.append(element[0])
							values.append(element[1])
						plt.title('Top des réclamations pour '+site+'\n pour la semaine '+num_semaine_mois_trimestre['semaine'], fontsize=16)
			elif num_semaine_mois_trimestre.keys()[0] == 'mois':
				if motif_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]:
						count = Counter(motif_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]).most_common(5)
						for element in count:
							labels.append(element[0])
							values.append(element[1])
						plt.title('Top des réclamations pour '+site+'\n pour le mois '+num_semaine_mois_trimestre['mois'], fontsize=16)
			elif num_semaine_mois_trimestre.keys()[0] == 'trimestre':
				if motif_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']]:
						count = Counter(motif_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']]).most_common(5)
						for element in count:
							labels.append(element[0])
							values.append(element[1])
						plt.title('Top des réclamations pour '+site+'\n pour le trimestre '+num_semaine_mois_trimestre['trimestre'], fontsize=16)

				# Construction du graphe
			if values :
				indexes = np.arange(len(labels))
				width = 1
				ax.set_ylim(0,max(values)+0.4*max(values))
				plt.legend(plt.bar(indexes, values, width, color=colors), labels, bbox_to_anchor=(1.13, 1), prop={'size':12})
				plt.xticks(indexes + width, '')
				plt.xlabel('Motifs de réclamations')
				plt.ylabel('Nombre de réclamations')
				plt.savefig('Graphiques/8-top_motifs-'+site+'-'+num_semaine_mois_trimestre.keys()[0]+'.png', dpi=120)
				#plt.show()
			plt.close()


	def tableau_recla(self, liste_recla_site_semaine, liste_recla_site_mois, liste_recla_site_trimestre, selection_site, num_semaine_mois_trimestre):
		#suppression des anciennes listes
		path = "ListeReclamations"
		files=os.listdir(path)
		for x in files:
			if not x in '0pageDeGarde.png' :
				print("haha")
				os.remove(path+'/'+x)


		styles = getSampleStyleSheet()
		style_titre = styles["Heading1"]
		for site in selection_site:
			if num_semaine_mois_trimestre.keys()[0] == 'semaine':
				if type(num_semaine_mois_trimestre.values()[0]) == type(list()):
					data = []
					if int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1]):
						num_semaines = []
						for j in range(int(num_semaine_mois_trimestre.values()[0][0]) > int(num_semaine_mois_trimestre.values()[0][1])+53):
							if j>53:
								num_semaines.append(j%53)
							else:
								num_semaines.append(j)
					else :
						num_semaines = range(int(num_semaine_mois_trimestre.values()[0][0]),int(num_semaine_mois_trimestre.values()[0][1])+1)
					for i in num_semaines:
						print i
						data = data + liste_recla_site_semaine[str(i)][site+str(i)]
						Title = Paragraph('Liste des réclamations pour '+site+' pour les semaines '+num_semaine_mois_trimestre.values()[0][0]+' à '+num_semaine_mois_trimestre.values()[0][1],
						style_titre)
				else:
						data = liste_recla_site_semaine[num_semaine_mois_trimestre['semaine']][site+num_semaine_mois_trimestre['semaine']]
						Title = Paragraph('Liste des réclamations pour '+site+' pour la semaine '+num_semaine_mois_trimestre['semaine'], style_titre)
			elif num_semaine_mois_trimestre.keys()[0] == 'mois':
					data = liste_recla_site_mois[num_semaine_mois_trimestre['mois']][site+num_semaine_mois_trimestre['mois']]
					Title = Paragraph('Liste des réclamations pour '+site+' pour le mois '+num_semaine_mois_trimestre['mois'], style_titre)
			elif num_semaine_mois_trimestre.keys()[0] == 'trimestre':
				data = liste_rela_site_trimestre[num_semaine_mois_trimestre['trimestre']][site+num_semaine_mois_trimestre['trimestre']]
				Title = Paragraph('Liste des réclamations pour '+site+' pour le trimestre '+num_semaine_mois_trimestre['trimestre'], style_titre)

			doc = SimpleDocTemplate("ListeReclamations/liste_reclamations_"+site+".pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
			doc.pagesize = landscape(A4)
			elements = []
			style = TableStyle([('ALIGN',(0,0),(0,0),'LEFT'),
											 ('VALIGN',(0,0),(0,0),'TOP'),
											 ('TEXTCOLOR',(0,0),(0,0),"black"),
											 ('INNERGRID', (0,0), (-1,-1), 0.25, "black"),
											 ('BOX', (0,0), (-1,-1), 0.25, "black"),
											 ])

			s = getSampleStyleSheet()
			s = s["BodyText"]
			s.wordWrap = 'CJK'
			data2 = [[Paragraph(cell, s) for cell in row] for row in data]
			data2 = [['Nom et Prénom', 'Adresse', 'Date', 'Numéro de la tournée', 'Motif', 'Commentaires']] + data2
			t=Table(data2)
			t.setStyle(style)

			elements.append(Title)

			#Send the data and build the file
			elements.append(t)
			doc.build(elements)

	""" Fonction pour mettre tous les fichiers dun répertoire donné dans une liste """
	def listeImagesDossier(self,nomDossier) :
		listeImages=list()
		listeImages.append("0pageDeGarde.png")
		for element in os.listdir(nomDossier):
			if(element!="0pageDeGarde.png"):
				listeImages.append(element)
		listeImages.sort()
		return listeImages

	"Fonction permettant d'afficher toutes les images dans un pdf"
	def fromPNGToPDF(self,pdfFileName, listImages, dir = ''):

		if (dir):
			dir += "/"

		cover = Image.open(dir + "0pageDeGarde.png" )
		width, height = cover.size


		pdf = FPDF(unit = "pt", format = [width, height])


		for page in listImages:
			pdf.add_page()
			pdf.image(dir + str(page) , 0, 0)

		pdf.output( pdfFileName + ".pdf", "F")
