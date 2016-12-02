#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
from PIL import Image # Faire sudo pip install pillow pour utiliser cette librairie
from fpdf import FPDF # Faire sudo pip install fpdf pour utiliser cette librairie
from collections import Counter
import matplotlib.pyplot as plt # pour les graphes, faire sudo apt-get install python-matplotlib avant
import numpy as np
from datetime import datetime
from math import *

# Problème d'encodage
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Model :
    def __init__(self) :
        print("Le modèle est bien instancié")

    """ fonction de lecture du CSV """

    def  readDirectory(self) :
        listeFichiers=list()
    	for element in os.listdir("FichiersCSV/"):
    		listeFichiers.append(element)
    	return listeFichiers

    def readSites(self) :
        liste_sites=list()
        l_sites = csv.reader(open("liste_sites","rb"))
        for row in l_sites:
            liste_sites.append(row[0])
        return liste_sites



    def readCSV(self,nomFichier) :
    #	nomFichier=raw_input("Veuillez entrer le nom du fichier  que vous voulez analysez (suivi de l'extension ) :")


    	with open("FichiersCSV/"+nomFichier, 'rb') as csvfile:
    		bdd = csv.reader(csvfile, delimiter=';')

    		motif=[]

    		dates = {}
    		sites = {}

    		liste_sites = []

    		l_sites = csv.reader(open("liste_sites","rb"))
    		for row in l_sites:
    			liste_sites.append(row[0])

    		selection_sites = []

    		removeFiles()
    	#	ajoutSite(liste_sites)
    	#	supprimerSite(liste_sites)
    	#	selectionSites(liste_sites, sites, dates, selection_sites)
    		date_min_max = parcoursBDD(bdd, dates, sites, motif)
    		csvfile.seek(0)
    		semaines = calculNbSemaine(bdd, dates, date_min_max['date_min'], date_min_max['date_max'])
    		showMotifGraph(motif)
    		showSiteGraph(sites)
    	#	showWeekSiteGraph(semaines['semaines'], semaines['nombre de semaines'], selection_sites)

    # suppression des graphes dans le dossier
    def removeFiles(self):
    	path = "Graphiques"
    	files=os.listdir(path)
    	for x in files:
    		if not x in '0pageDeGarde.png':
        			os.remove(path+'/'+x)

    # ajout d'un site dans le fichier et dans la liste courante
    def ajoutSite(self,liste_sites):
    	question = raw_input("Souhaitez-vous ajouter un site?")
    	if (question== "oui" or question =="OUI" or question =="O" or question=="o" or question=="yes"):
    		site = raw_input("Entrez le nom du site: ")
    		site = site.upper()
    		liste_sites.append(site)
    		c = csv.writer(open("liste_sites", "a"))
    		c.writerow([site])

    # suppression d'un site dans le fichier et dans la liste courante
    def supprimerSite(self,liste_sites):
    	question = raw_input("Souhaitez-vous supprimer un site?")
    	if (question== "oui" or question =="OUI" or question =="O" or question=="o" or question=="yes"):
    		site = raw_input("Entrez le nom du site: ")
    		site = site.upper()
    		fichier = open("liste_sites", "rb")
    		c_write = csv.writer(open("liste_sites_temp", "a"))
    		c_read = csv.reader(fichier, delimiter=';')

    		#ext ce que le site est présent dans la liste ?
    		while site not in liste_sites:
    			site = raw_input("Ce site n\'est pas présent dans la liste, entrez le nom du site: ")
    			site = site.upper()

    		#suppresion de la liste des sites sans relire le fichier
    		liste_sites.remove(site)

    		#ecriture de la nouvelle liste dans un fichier temporaire puis suppression
    		for row in c_read:
    			if site not in row[0]:
    				c_write.writerow(row)
    		os.remove("liste_sites")
    		os.renames("liste_sites_temp", "liste_sites")


    def selectionSites(self,liste_sites, sites, dates, selection_sites):
    	#ajout du site s'il est demandé
    	for site in liste_sites:
    		question = raw_input("Souhaitez-vous les indicateurs pour "+site+" ?")
    		if (question== "oui" or question =="OUI" or question =="O" or question=="o" or question=="yes"):
    			sites[site] = []
    			dates[site] = []
    			selection_sites.append(site)

    """ Parcours du fichier BDD et récupération des infos """
    def parcoursBDD(self,bdd, dates, sites, motif):

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
    					if '' != row[13]:
    						sites[site].append(row[13])
    						dates[site].append([row[13], date, site])

    	return {'date_min':date_min, 'date_max':date_max}


    """ Détermination de la semaine du motif et par site """
    def calculNbSemaine(self,bdd, dates, date_min, date_max):
    	diff = date_max - date_min
    	nb_jours = diff.days
    	nb_semaines = int(ceil(nb_jours/7.0)) # arrondi supérieur

    	semaines = []
    	for i in range(1, nb_semaines+2):
    		lieux = {}
    		for site in dates:
    			lieux[site+str(i-1)] = [] #besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
    		semaines.append(lieux)

    	for rows in dates :
    		for row in dates[rows]:
    			diff_date = row[1] - date_min
    			semaine = int(ceil(diff_date.days/7.0))
    			semaines[semaine][rows+str(semaine)].append(row[0])
    	return {'semaines': semaines, 'nombre de semaines': nb_semaines}


    """ Initialisation d'un tableau de semaines avec dans chaque semaine les tableaux de chaque site,
    	parcours de dates, determination de la semaine ( diff entre date min puis division par 7 pour avoir la semaine et insertion dans le tableau """



    """ Calcul du nombre de réclamations par motif et affichage sur un même graphe """
    def showMotifGraph (self,motif):

    	# Calcul du nombre de reclamation par motifs
    	nb_recla_motifs = Counter(motif[1:len(motif)])
    	name = nb_recla_motifs.keys()

    	data = nb_recla_motifs.values()
    	# Construction du camembert

    	explode= np.zeros(len(nb_recla_motifs))
    	plt.pie(data, explode=explode, labels=name, autopct = lambda x: str(round(x, 1)) + '%', shadow=False)
    	plt.axis('equal')
    	plt.title('nb_recla_motifs')
    	plt.savefig('Graphiques/' + 'nb_recla_motifs.png', fontsize='20')
    	plt.show()
    	plt.close()

    """ Calcul du nombre de réclamations par site et affichage des graphes pour chaque site dans un png
    """
    def showSiteGraph(self,sites) :
    	for site in sites:
    		count_sites = Counter(sites[site])
    		name = count_sites.keys()
    		data = count_sites.values()

    		# Construction du camembert

    		explode = np.zeros(len(count_sites))
    		plt.pie(data, explode=explode, labels=name, autopct = lambda x: str(round(x, 1)) + '%', 		shadow=False)
     		plt.axis('equal')
    		plt.title('Nombre de réclamations par motifs pour '+site)
    		plt.savefig('Graphiques/'+site+'.png')
    		plt.show()
    		plt.close()

    # Calcul du nombre de réclamations par site pour une semaine et affichage des graphes pour chaque site dans un png
    def showWeekSiteGraph(self,semaines, nb_semaines, liste_sites):
    	num_semaine = raw_input('Pour quelle semaine souhaitez-vous voir les indicateurs ?')
    	while int(num_semaine) > nb_semaines:
    		print("Cette semaine n'est pas traitée dans le fichier")
    		num_semaine = raw_input('Pour quelle semaine souhaitez-vous voir les indicateurs ?')

    	for site in liste_sites :
    		if semaines[int(num_semaine)][site+num_semaine]:
    			count = Counter(semaines[int(num_semaine)][site+num_semaine])
    			name = count.keys()
    			data = count.values()

    			# Construction du camembert

    			explode = np.zeros(len(data))
    			plt.pie(data, explode=explode, labels=name, autopct = lambda x: str(round(x, 1)) + '%', 		shadow=False)
    	 		plt.axis('equal')
    			plt.title('Nombre de réclamations par motifs pour '+site+' par semaine ')
    			plt.savefig('Graphiques/'+site+'-semaine.png')
    			plt.show()
    			plt.close()
    		else:
    			print("Il n'y a pas de réclamations pour "+site+" sur la semaine "+num_semaine)



    """ Fonction pour mettre tous les fichiers d'un répertoire donné dans une liste """
    def listeImagesDossier(self,nomDossier) :
    	listeImages=list()
    	listeImages.append("0pageDeGarde.png")
    	for element in os.listdir(nomDossier):
    		if(element!="0pageDeGarde.png"):
    			listeImages.append(element)
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
