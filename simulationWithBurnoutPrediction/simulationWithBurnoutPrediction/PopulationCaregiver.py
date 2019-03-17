# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:35:49 2018

@author: Oussama BATATA
"""

# import library .........

import numpy as np

import InputData
import Caregiver
import ServiceOfRespite


class PopulationCaregiver:
    """Classe définiss un aidant (caregiver) caractérisée par :

    - nbCluster = Nbr de classes d'aidants

    - nbrStatePerCluster  = pour chaque classe le nombre d'état de la chaîne de Markov peut être spéciphique

    - nbCaregiverPerCluster = nombre d'aidants pour chaque classe d'aidants

    - timeHorizon = SLe nombre de pas de temps de notre simulation

    - listeCaregiver = la liste contenant les aidants et leurs attributs

    - markovMatrix = la matrice de %markov pour les probabilities de transitions entre les états dépuisement

    - durationInHospital =  La durée d'hospitalisation si l'a a fait à son patient"""





    def __init__(self, inputData, serviceRepit):  # Notre méthode constructeur
        # -------------------------------------

        ## attributs pour acceder à la classe inputData
        self.__inpuData = inputData

        self.__serviceRepit = serviceRepit
        #self.__respiteHome = respiteHome
        ## attributs de la class de la population en entier

        self.__nbCluster = 0
        self.__nbrStatePerCluster = 0
        self.__nbCaregiversPerCluster = 0
        self.__timeHorizon = 0;
        self.__listeCaregivers = [] # Cette liste contient tout les caregivers avec leur cluster et idClusyter confondu
        self.__matrixOfCaregivers = [] # Cette liste contient des listes de cluster d'aidants, chaque liste contient les caregivers de son cluster
        self.__markovMatrix = []
        # -----------------------------------



    """"  Fcontion pour importer les données  """
    def importData (self):
        self.__nbCluster = self.__inpuData.getNuberCluster()
        self.__nbrStatePerCluster = self.__inpuData.getNberStatePerCluster()
        self.__nbCaregiversPerCluster = self.__inpuData.getNbCaregiversPerCluster()
        self.__timeHorizon = self.__inpuData.getTimeHorizion()
        self.__listeCaregivers = self.__inpuData.getListeCaregivers()
        self.__markovMatrix = self.__inpuData.getMarkovMatrix()
        self.__burnoutCaregivers = self.__inpuData.getBurnoutCaregivers()

    '''---------------------Mes fonction gets en dehors de la calss-----------------------------'''
    #self.__nbCluster
    def getNbCluster(self):
        return self.__nbCluster

    #self.__nbrStatePerCluster
    def getNbStateOerCluster(self):
        return self.__nbrStatePerCluster

    #self.__nbCaregiversPerCluster
    def getNbCaregiversPerCluster(self):
        return self.__nbCaregiversPerCluster

    #self.__timeHorizon
    def getTimeHorizon(self):
        return self.__timeHorizon

    #self.__listeCaregivers
    def getListeCaregiver(self):
        return self.__listeCaregivers

    #self.__burnoutCaregivers
    def getBurnoutCaregivers(self):
        return self.__burnoutCaregivers

    #self.__matrixOfCaregivers
    def getMatrixOfCaregivers(self):
        return self.__matrixOfCaregivers

    #self.__markovMatrix
    def getMarkovMatrix(self):
        return self.__markovMatrix

    ''' --------------------------------------------Fin de mes fonctions getters ------------------------------'''



    def generatePopulation(self):
        id = 0
        for i in range(self.__nbCluster):
            tableTemp = []
            for j in range(self.__nbCaregiversPerCluster):
                caregiver = Caregiver.Caregiver(id, i, j, self.__burnoutCaregivers[i][j][0], self.__serviceRepit)
                id+=1
                self.__listeCaregivers.append(caregiver)
                tableTemp.append(caregiver)
            self.__matrixOfCaregivers.append(tableTemp)


    def getCaregiverByTwoId(self, idCluster, idIncluster):
        for i in self.__listeCaregivers:
            if i.idCluster == idCluster and i.idInCluster == idIncluster :
                return i



    def updateStateCaregiver(self, idCluster, idInCluster, timePeriod, caregiver):
        '''print("je rentre dans l'update state de l'aidant suivant :")
        print(self.__matrixOfCaregivers[idCluster][idInCluster])'''

        valRand = np.random.randint(0,10)/10
        #print("ma val rand est : "+str(valRand))
        sommeCumul = 0
        #caregiver = self.__matrixOfCaregivers[idCluster][idInCluster]
        line = int(caregiver.getBurnout() -1)

        #print("ligne dans la matrice de Markov"+str(self.__markovMatrix[idCluster][timePeriod]))
        it = 0
        #print("la matrice de transtions à la ligne est : " +str(self.__markovMatrix[idCluster][timePeriod][line]))
        while it < len(self.__markovMatrix[idCluster][timePeriod][line]):
            sommeCumul+=self.__markovMatrix[idCluster][timePeriod][line][it]
            #print("ma somme cumul est :"+str(sommeCumul))
            if valRand <= sommeCumul:
                caregiver.setBurnout(float(it+1))
                #print("apres transition l'aidant est comme suit")
                #print(self.__matrixOfCaregivers[idCluster][idInCluster])
                break
            it+=1


    def printTableCaregivers(self):

        for i in range(5):
            print('*'*33)
            print(self.__listeCaregivers[i])







    def __repr__(self):
        return " La classe Population of caregiver comporte: nbCluster({}), nbCaregiverPerCluster({}), nbStatesPerCluster({}), timeHorizon({})".format(self.__nbCluster, self.__nbCaregiversPerCluster, self.__nbrStatePerCluster,
                                                                                          self.__timeHorizon)






