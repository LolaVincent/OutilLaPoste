#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
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

colors=['coral', 'lightpink', 'salmon', 'burlywood', 'indianred', 'tomato', 'lightsage', 'sandybrown', 'khaki', 'thistle', 'tan', 'darksalmon', 'lightcoral', 'lightblue', 'lightsalmon', 'rosybrown', 'lightgrey'  ]


class Model :
    def __init__(self) :
        print("Le modèle est bien instancié")
        self.listeSitesCoches=list()


    """ fonction de lecture du CSV """

    def  readDirectory(self) :
        listeFichiers=list()
    	for element in os.listdir("FichiersCSV/"):
    		listeFichiers.append(element)
    	return listeFichiers

    def readSites(self) :
        liste_sites=[]
        l_sites = csv.reader(open("liste_sites","rb"))
        for row in l_sites:
            liste_sites.append(row[0])
        return liste_sites





    def readCSV(self,nomFichier,listeSitesCoches,choixPeriode,valeurPeriode) :
    #	nomFichier=raw_input("Veuillez entrer le nom du fichier  que vous voulez analysez (suivi de l'extension ) :")
        self.listeSitesCoches=listeSitesCoches

        with open("FichiersCSV/"+nomFichier, 'rb') as csvfile:

            bdd = csv.reader(csvfile, delimiter=';')
            motif=[]
            sites = {}
            tournee_site_date={}
            motif_site_date = {}
            liste_sites = []
            selection_site = []

            #Suppression des graphes dans le dossier
            self.removeFiles()

            #lecture de la liste des sites
            l_sites = csv.reader(open("liste_sites","rb"))
            for row in l_sites:
    			liste_sites.append(row[0])



    	#	self.ajoutSite()
    	#	self.supprimerSite()
            self.selectionSites(liste_sites, sites, motif_site_date, tournee_site_date, selection_site)

            # détermination des dates min et max et du nombre de semaines
    		#lecture du csv : lecture des motifs, separation par site
            date_min_max = self.parcoursBDD(bdd, sites, motif_site_date, tournee_site_date, motif)
            mois_min = date_min_max['date_min'].month
    #        csvfile.seek(0)
            nb = self.calculNbSemaine(date_min_max['date_min'], date_min_max['date_max'])
            nb_semaine = nb['nb_semaines']
            nb_mois= nb['nb_mois']
            print(date_min_max)
            print(mois_min)
            print(nb)
            print(nb_semaine)
            print(nb_mois)
		    # Calcul des indicateurs


            motif_site = self.motifSitesSemaines(nb_mois, nb_semaine, mois_min, date_min_max['date_min'], motif_site_date)
            motif_site_semaine = motif_site['motif_site_semaine']
            motif_site_mois = motif_site['motif_site_mois']

            nb_motif_semaine = self.nbReclaSemaine(motif_site_semaine, nb_semaine)
            tournee_site = self.tourneeSitesSemaines(nb_mois, nb_semaine, mois_min, date_min_max['date_min'],  tournee_site_date)

            tournee_site_semaine = tournee_site['tournee_site_semaine']
            tournee_site_mois = tournee_site['tournee_site_mois']



		    #choix de la semaine
            print("LIS CE QU'IL Y A ICI JUSTE EN BAS DE CE COMMENTAIRE")
            #ici on récupère un dico faudra bien faire attention à comment le récupérer avec tes MessageBox
            num_semaine_mois = self.choixSemaineMois(nb_semaine,choixPeriode,valeurPeriode)

            self.showMotifGraph(motif)
            self.showNbReclaSemaineGraph(nb_motif_semaine)
            self.showSiteGraph(sites)
            self.showMotifSiteWeekGraph(motif_site_semaine, motif_site_mois, selection_site, num_semaine_mois)
            self.showTopMotifSiteGraph(motif_site_semaine,motif_site_mois,selection_site,num_semaine_mois)
            self.showTourneeSiteWeekGraph(tournee_site_semaine, tournee_site_mois, selection_site, num_semaine_mois)

    def showTopMotifSiteGraph(self,motif_site_semaine,motif_site_mois,selection_site,num_semaine_mois):
    	for site in selection_site:
    		labels = []
    		values = []
    		if num_semaine_mois.keys()[0] == 'semaine':
    			if type(num_semaine_mois.values()[0]) == type(list()):
    				semaines = {}
    				semaines[site] = []
    				for i in range(int(num_semaine_mois.values()[0][0]), int(num_semaine_mois.values()[0][1])):
    					for motif in motif_site_semaine[i][site+str(i)]:
    						semaines[site].append(motif)
    				count = Counter(semaines[site]).most_common(5)

    				for element in count:
    					labels.append(element[0])
    					values.append(element[1])

    			elif motif_site_semaine[int(num_semaine_mois['semaine'])][site+num_semaine_mois['semaine']]:
    					count = Counter(motif_site_semaine[int(num_semaine_mois['semaine'])][site+num_semaine_mois['semaine']]).most_common(5)

    					for element in count:
    						labels.append(element[0])
    						values.append(element[1])
    		elif num_semaine_mois.keys()[0] == 'mois':
    			if motif_site_mois[int(num_semaine_mois['mois'])][site+num_semaine_mois['mois']]:
    					count = Counter(motif_site_mois[int(num_semaine_mois['mois'])][site+num_semaine_mois['mois']]).most_common(5)
    					for element in count:
    						labels.append(element[0])
    						values.append(element[1])

    			# Construction du graphe

    		indexes = np.arange(len(labels))
    		width = 1
    		plt.legend(plt.bar(indexes, values, width, color=colors), labels, bbox_to_anchor=(1.13, 1), prop={'size':9})
    		plt.title('Top 5 des réclamations par tournee \n pour '+site+' par semaine ', fontsize=16)
    		plt.savefig('Graphiques/5-tournee-'+site+'-semaine.png')
    		#plt.show()
    		plt.close()


    def showNbReclaSemaineGraph(self,nb_recla_semaine):

    	# Calcul du nombre de reclamation par motifs
    	nb_recla= Counter(nb_recla_semaine)
    	nb_recla=sorted(nb_recla.items(),key=lambda t : t[0])

    	#data = nb_recla.values()
    	# Construction du camembert

    	labels = []
    	values = []
        for element in nb_recla:
            labels.append(element[0])
            values.append(element[1])
    	indexes = np.arange(len(labels))
    	width = 1
    	plt.bar(indexes, values, width, color=colors)
    	plt.xticks(indexes + width * 0.5, labels)
    	#plt.axis('equal')

    	plt.title('nombre de réclamations par semaine',fontsize=20)
    	plt.savefig('Graphiques/' + '2-nb_recla_semaine.png', fontsize='20')
        #plt.show()
        plt.close()
    # suppression des graphes dans le dossier
    def removeFiles(self):
    	path = "Graphiques"
    	files=os.listdir(path)
    	for x in files:
            if not x in '0pageDeGarde.png' :
                print("haha")
                os.remove(path+'/'+x)

    # ajout d'un site dans le fichier et dans la liste courante
    def ajoutSite(self, nomNouveauFichier):
    	site = nomNouveauFichier
    	site = site.upper()
    	#liste_sites.append(site)
    	c = csv.writer(open("liste_sites", "a"))
    	c.writerow([site])

    # suppression d'un site dans le fichier et dans la liste courante
    def supprimerSite(self,nomFichierSupprime):
    	site = nomFichierSupprime
    	site = site.upper()
    	fichier = open("liste_sites", "rb")
    	c_write = csv.writer(open("liste_sites_temp", "a"))
    	c_read = csv.reader(fichier, delimiter=';')

    	#ecriture de la nouvelle liste dans un fichier temporaire puis suppression
    	for row in c_read:
    		if site not in row[0]:
    			c_write.writerow(row)
    	os.remove("liste_sites")
    	os.renames("liste_sites_temp", "liste_sites")


    def selectionSites(self,liste_sites, sites, motif_site_date, tournee_site_date, selection_site):
    	#ajout du site s'il est demandé
        print(liste_sites)
        print(self.listeSitesCoches)
        for site in self.listeSitesCoches:
    #		question = raw_input("Souhaitez-vous les indicateurs pour "+site+" ?")
    #		if (question== "oui" or question =="OUI" or question =="O" or question=="o" or question=="yes"):
            sites[site] = []
            tournee_site_date[site] = []
            motif_site_date[site]=[]
            selection_site.append(site)
        print(selection_site)
        print(motif_site_date)
        print(tournee_site_date)
        print(sites)

    """ Parcours du fichier BDD et récupération des infos """
    def parcoursBDD(self,bdd, sites, motif_site_date, tournee_site_date, motif):

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
                            motif_site_date[site].append([row[13], date])
                        if '' != row[47]:
                            tournee_site_date[site].append([row[47], date])

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

    """ Détermination de la semaine du motif et par site """
    """ Anciennne version de calculNbSemaine
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
        """

    """ Initialisation d'un tableau de semaines avec dans chaque semaine les tableaux de chaque site,
    	parcours de dates, determination de la semaine ( diff entre date min puis division par 7 pour avoir la semaine et insertion dans le tableau """



    """ Calcul du nombre de réclamations par motif et affichage sur un même graphe """
    def showMotifGraph (self,motif):
        print("HAHAHAHAH On est dans le code de Show Motif graph motherfucker")

    	# Calcul du nombre de reclamation par motifs
    	nb_recla_motifs = Counter(motif[1:len(motif)])
    	name = nb_recla_motifs.keys()

    	data = nb_recla_motifs.values()
    	# Construction du camembert

    	explode= np.zeros(len(nb_recla_motifs))

        plt.figure(figsize=(12,10))
    	plt.pie(data, explode=explode, autopct = lambda x: str(round(x, 1)) + '%', shadow=False, colors=colors)
    	#plt.axis('equal')
    	plt.title('Nombre de réclamations par motif pour l\'ensemble des sites', fontsize=20)
        plt.legend(name,bbox_to_anchor=(1.13,0.30),prop={'size':9})
        plt.savefig('Graphiques/1-' + 'nb_recla_motifs.png', dpi=120)
        print("On est à la fin de showmotifgraph juste avant le show")
    	#plt.show()
        print("On est à la fin de showmotifgraph juste avant le close")
    	plt.close()
        print("On est à la fin de showmotifgraph juste après le close")


    """ Calcul du nombre de réclamations par site et affichage des graphes pour chaque site dans un png
    """
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
                plt.savefig('Graphiques/3-'+site+'.png', fontsize='20', dpi=120)
		plt.close()








    """
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
    			#plt.show()
    			plt.close()
    		else:
    			print("Il n'y a pas de réclamations pour "+site+" sur la semaine "+num_semaine)
        """

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
    	return num

    # Calcul du nombre de réclamations par site pour une semaine et affichage des graphes pour chaque site dans un png

    def showMotifSiteWeekGraph(self,motif_site_semaine, motif_site_mois, selection_site, num_semaine_mois):
    	for site in selection_site:
    		if num_semaine_mois.keys()[0] == 'semaine':
    			if type(num_semaine_mois.values()[0]) == type(list()):
    				semaines = {}
    				semaines[site] = []
    				for i in range(int(num_semaine_mois.values()[0][0]), int(num_semaine_mois.values()[0][1])):
    					for motif in motif_site_semaine[i][site+str(i)]:
    						semaines[site].append(motif)
    				count = Counter(semaines[site])
    				name = count.keys()
    				data = count.values()

    			elif motif_site_semaine[int(num_semaine_mois['semaine'])][site+num_semaine_mois['semaine']]:
    					count = Counter(motif_site_semaine[int(num_semaine_mois['semaine'])][site+num_semaine_mois['semaine']])
    					name = count.keys()
    					data = count.values()
    		elif num_semaine_mois.keys()[0] == 'mois':
    			if motif_site_mois[int(num_semaine_mois['mois'])][site+num_semaine_mois['mois']]:
    					count = Counter(motif_site_mois[int(num_semaine_mois['mois'])][site+num_semaine_mois['mois']])
    					name = count.keys()
    					data = count.values()


    		# Construction du camembert

    		explode = np.zeros(len(data))
                plt.figure(figsize=(12,10))
    		plt.pie(data, explode=explode, autopct = lambda x: str(round(x, 1)) + '%', 		shadow=False, colors=colors)
    	 	#plt.axis('equal')
    		plt.title('Nombre de réclamations par motifs \n pour '+site+' par semaine \n', fontsize=16)
    		plt.savefig('Graphiques/4-motif-'+site+'-semaine.png')
		plt.close()



    def showTourneeSiteWeekGraph(self,tournee_site_semaine, tournee_site_mois, selection_site, num_semaine_mois):
    	for site in selection_site:
    		if num_semaine_mois.keys()[0] == 'semaine':
    			if type(num_semaine_mois.values()[0]) == type(list()):
    				semaines = {}
    				semaines[site] = []
    				for i in range(int(num_semaine_mois.values()[0][0]), int(num_semaine_mois.values()[0][1])):
    					for tournee in tournee_site_semaine[i][site+str(i)]:
    						semaines[site].append(tournee)
    				count = Counter(semaines[site])
    				name = count.keys()
    				data = count.values()

    			elif tournee_site_semaine[int(num_semaine_mois['semaine'])][site+num_semaine_mois['semaine']]:
    					count = Counter(tournee_site_semaine[int(num_semaine_mois['semaine'])][site+num_semaine_mois['semaine']])
    					name = count.keys()
    					data = count.values()
    		elif num_semaine_mois.keys()[0] == 'mois':
    			if motif_site_mois[int(num_semaine_mois['mois'])][site+num_semaine_mois['mois']]:
    				count = Counter(motif_site_mois[int(num_semaine_mois['mois'])][site+num_semaine_mois['mois']])
    				name = count.keys()
    				data = count.values()


    			# Construction du camembert
    		labels = name
    		values = data

    		indexes = np.arange(len(labels))
    		width = 1

    		plt.bar(indexes, values, width, color=colors)
    		plt.xticks(indexes + width * 0.5, labels)
     		#plt.axis('equal')
    		plt.title('Nombre de réclamations par tournee \n pour '+site+' par semaine \n', fontsize=16)
    		plt.savefig('Graphiques/tournee-'+site+'-semaine.png')
		plt.close()



    def motifSitesSemaines(self,nb_mois, nb_semaine, mois_min, date_min, motif_site_date):
        motif_site_semaine = []
        motif_site_mois = []
        for i in range(1, nb_semaine+2):
        	motif_lieu = {}
        	for site in motif_site_date:
        		motif_lieu[site+str(i-1)] = []
                #besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
        	motif_site_semaine.append(motif_lieu)

        for i in range(1, nb_mois+2):
        	motif_lieu = {}
        	for site in motif_site_date:
        		motif_lieu[site+str(i-1)] = []
        #besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
        	motif_site_mois.append(motif_lieu)


        for rows in motif_site_date :
        	for row in motif_site_date[rows]:
        		diff_date = row[1] - date_min
        		semaine = int(ceil((diff_date.days + 1)/7.0))
        		motif_site_semaine[semaine][rows+str(semaine)].append(row[0])
        		mois = row[1].month - mois_min + 1
        		motif_site_mois[mois][rows+str(mois)].append(row[0])
        return {'motif_site_semaine': motif_site_semaine, 'motif_site_mois': motif_site_mois}

    def nbReclaSemaine(self,motif_site_semaine, nb_semaine):
        nb_motif_semaine = {}
        for i in range(1, nb_semaine+1):
        	print i
        	somme = 0
        	for site in motif_site_semaine[i]:
        		somme = somme + len(motif_site_semaine[i][site])
        	nb_motif_semaine['semaine '+str(i)] = somme
        return nb_motif_semaine

    def tourneeSitesSemaines(self,nb_mois, nb_semaine, mois_min, date_min, tournee_site_date):
    	tournee_site_semaine = []
    	tournee_site_mois = []
    	for i in range(1, nb_semaine+2):
    		tournee_lieu = {}
    		for site in tournee_site_date:
    			tournee_lieu[site+str(i-1)] = []
    #besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
    		tournee_site_semaine.append(tournee_lieu)

    	for i in range(1, nb_mois+2):
    		tournee_lieu = {}
    		for site in tournee_site_date:
    			tournee_lieu[site+str(i-1)] = []
    #besoin de différencier le site pour chaque semaine sinon agit sur tous car même clé
    		tournee_site_mois.append(tournee_lieu)

    	for rows in tournee_site_date :
    		for row in tournee_site_date[rows]:
    			diff_date = row[1] - date_min
    			semaine = int(ceil((diff_date.days + 1)/7.0))
    			tournee_site_semaine[semaine][rows+str(semaine)].append(row[0])
    			mois = row[1].month - mois_min + 1
    			tournee_site_mois[mois][rows+str(mois)].append(row[0])
    	return {'tournee_site_semaine': tournee_site_semaine, 'tournee_site_mois': tournee_site_mois}
