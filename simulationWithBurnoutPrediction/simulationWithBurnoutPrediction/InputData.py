# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:35:49 2018

@author: Oussama BATATA
"""

# import library .........

#import numpy as np
#imort pandas as pd






class InputData:
    """Classe définiss un aidant (caregiver) caractérisée par :

    - nbCluster = Nbr de classes d'aidants

    - nbrStatePerCluster  = pour chaque classe le nombre d'état de la chaîne de Markov peut être spéciphique

    - nbCaregiverPerCluster = nombre d'aidants pour chaque classe d'aidants

    - timeHorizon = SLe nombre de pas de temps de notre simulation


    - listeCaregiver = la liste contenant les aidants et leurs attributs

    - markovMatrix = la matrice de %markov pour les probabilities de transitions entre les états dépuisement


       """




    """"  Déclaration des attributs de ma classe """
    def __init__(self):  # Notre méthode constructeur
        # -------------------------------------
        ## attributs de la class de la population en entier

        self.__nbCluster = 0
        self.__nbrStatePerCluster = 0
        self.__nbCaregiversPerCluster = 0
        self.__timeHorizon = 0
        self.__listeCaregivers = []
        self.__markovMatrix = []
        self.__burnoutCaregivers = []
        # -----------------------------------

      ## Les données pour construire un ensemble de services de répit plus un hôpital

        self.__nbrRespiteServices = 0
        self.__maxTimeOfRespiteCare = 0
        # -----------------------------------

       ## Les données de notre simulation
        self.__frequenceRespit = 0
        self.__nbReplication = 0
        # -----------------------------------








    """"  Fcontion pour importer les données  """

    def importData(self):

        mon_fichier = open("C:/Users/oussama.batata/eclipse-workspace/simulation/dataInput.txt", "r")
        contenu = mon_fichier.read().split(" ")
        mon_fichier.close()

        self.__nbCluster = int(contenu[0])
        self.__nbCaregiversPerCluster = int(contenu[1])
        self.__nbrStatePerCluster = int(contenu[2])
        self.__timeHorizon = int(contenu[3])
        self.__nbrRespiteServices = int(contenu[4])
        self.__frequenceRespit = float(contenu[5])
        self.__nbReplication = int(contenu[6])
        self.__maxTimeOfRespiteCare = int(contenu[7])

        ## APrès le chargement des données requis pour les classes, nous allons importer note chaîne de Mzrkov

        print("Lire la matrice de Markov")
        mon_fichier = open("C:/Users/oussama.batata/eclipse-workspace/simulation/Markovmatrix.txt", "r")
        contenuMarkovmatrix = mon_fichier.read().split(" ")
        mon_fichier.close()

        s = 0
        for i in range(self.__nbCluster):
            temp1 = []
            for j in range(self.__timeHorizon-1):
                temp2 = []
                for k in range(self.__nbrStatePerCluster):
                    temp3 = []
                    for l in range(self.__nbrStatePerCluster):
                        temp3.append(float(contenuMarkovmatrix[s]))
                        s += 1
                    temp2.append(temp3)
                temp1.append(temp2)
            self.__markovMatrix.append(temp1)

        ## Chargement des données de l'épuisement des aidants au cours du temps;


        mon_fichier = open("C:/Users/oussama.batata/eclipse-workspace/simulation/burnoutCaregivers.txt", "r")
        contenuBurnoutCaregivers = mon_fichier.read().split(" ")
        mon_fichier.close()

        s = 0
        for i in range(self.__nbCluster):
            temp1 = []
            for j in range(self.__nbCaregiversPerCluster):
                temp2 = []
                for k in range(self.__timeHorizon):
                    temp2.append(float(contenuBurnoutCaregivers[s]))
                    s += 1
                temp1.append(temp2)

            self.__burnoutCaregivers.append(temp1)





#################################################################################################################################################
    def prinMarkovMatrix(self):
        ## Afficher la matrice de markov
        for i in range(self.__nbCluster):
            print("cluster-------------------------------------------------------------------")
            for j in range(self.__timeHorizon - 1):
                print("time horizon -------------------------")
                for k in range(self.__nbrStatePerCluster):
                    print(self.__markovMatrix[i][j][k])









    ''' Mes getters pour acceter au attributs de ma class depuis l'éxterieur !!!!!'''

        ##self.__nbCluster
    def getNuberCluster(self):
        return self.__nbCluster

        #self.__nbrStatePerCluster
    def getNberStatePerCluster(self):
        return self.__nbrStatePerCluster

        #self.__nbCaregiversPerCluster
    def getNbCaregiversPerCluster(self):
        return self.__nbCaregiversPerCluster

        #self.__timeHorizon
    def getTimeHorizion(self):
        return self.__timeHorizon

        #self.__listeCaregivers
    def getListeCaregivers(self):
        return self.__listeCaregivers

        #self.__markovMatrix
    def getMarkovMatrix(self):
        return self.__markovMatrix

        #self.__burnoutCaregivers
    def getBurnoutCaregivers(self):
        return self.__burnoutCaregivers
        # -----------------------------------
        #self.__nbrRespiteServices
    def getNbRespiteServices(self):
        return self.__nbrRespiteServices

        #self.__maxTimeOfRespiteCare
    def getMaxTimeRespiteCare(self):
        return self.__maxTimeOfRespiteCare
        # -----------------------------------
        #self.__frequenceRespit
    def getFrequenceRespit(self):
        return self.__frequenceRespit

        #self.__nbReplication
    def getNbReplication(self):
        return  self.__nbReplication
        # -----------------------------------




    """"  Fcontion pour afficher les données  """

    def __repr__(self):
        return " La classe data comporte: nbCluster({}), nbCaregiverPerCluster({}), nbStatesPerCluster({}), timeHorizon({})," \
               "nbRespiteServices({}), fréquenceRespit({}), tempsDeRépitMax({}), nbReplication({})".format(self.__nbCluster, self.__nbCaregiversPerCluster, self.__nbrStatePerCluster,
                                                                                          self.__timeHorizon, self.__nbrRespiteServices, self.__frequenceRespit,
                                                                                          self.__maxTimeOfRespiteCare, self.__nbReplication)


