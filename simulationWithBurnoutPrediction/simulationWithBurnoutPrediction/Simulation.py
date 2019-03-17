# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:35:49 2018

@author: Oussama BATATA
"""

# import library .........

#import numpy as np
#imort pandas as pd
import pandas as pd
import numpy as np
import os
import math
import pydot
import io
from IPython.display import Image # Pour afficher une image dans le notebook
from os import system # Pour faire référence à l'OS windos et au prgramme existant sur le PC (ex: graphviz)
import graphviz
from scipy import stats
import statistics
import math
import seaborn as sns
import matplotlib.pyplot as plt
from operator import itemgetter

import copy

import seaborn as sns


from scipy.interpolate import interp1d
import InputData
import PopulationCaregiver
import Caregiver
import numpy as np

sns.set_style("darkgrid")




class Simulation:
    """Classe définiss un aidant (caregiver) caractérisée par :

    - timeHorizon = Horizon de temps

    - nbrReplication = Nombre de réplication pour valider statistiquement nos résultats"""





    def __init__(self, inputData, populationOfCaregivers, serviceRepit):  # Notre méthode constructeur
        # -------------------------------------

        ## attributs pour acceder à la classe inputData
        self.__inpuData = inputData
        self.__populationOfCaregivers = populationOfCaregivers
        self.__serviceRepit = serviceRepit
        ##Attributs de la classe Simulation

        self.__timeHorizon = self.__inpuData.getTimeHorizion()
        self.__nbReplication = self.__inpuData.getNbReplication()

        ## attributs utiles pour la classe

        self.__nbCluster = self.__inpuData.getNuberCluster()
        self.__nbrStatePerCluster = self.__inpuData.getNberStatePerCluster()
        self.__nbCaregiversPerCluster = self.__inpuData.getNbCaregiversPerCluster()
        self.__listeCaregivers = copy.deepcopy(self.__inpuData.getListeCaregivers())
        self.__markovMatrix = self.__inpuData.getMarkovMatrix()
        self.__burnoutCaregivers = self.__inpuData.getBurnoutCaregivers()

        self.__matrixOfCaregivers = copy.deepcopy(self.__populationOfCaregivers.getMatrixOfCaregivers())
        self.__listeAttenteCaregiver = self.__serviceRepit.getFilleAtteteRespiteService()
        # -----------------------------------
        self.__kpisimulation1 = np.zeros((self.__nbCluster, self.__nbrStatePerCluster, self.__timeHorizon-1))
        self.__kpiRealite1 = np.zeros((self.__nbCluster, self.__nbrStatePerCluster, self.__timeHorizon))

        self.__kpiReplicateSimulation = []


    ## Récuprer le KPI dans la réalité !
    def getKpiInRealite(self):
        for i in range(self.__nbCluster):
            for j in range(self.__nbCaregiversPerCluster):
                for k in range(self.__timeHorizon):
                    burnoutLevel = int(self.__burnoutCaregivers[i][j][k])-1

                    '''print("burnoutlevel : "+str(burnoutLevel))
                    print("Kpi a cet case est : "+str(self.__kpiRealite1[i][burnoutLevel][k]))'''
                    self.__kpiRealite1[i][burnoutLevel][k]+=1



#### Juster poura debeuguer le code , sur une seule réplication ==>> une seule simulation
    #######################################################
    ######################################################
    def plotRealiteEtSimulation(self, realite, simulation):
        #print("checker")
        indices = np.arange(len(realite) - 1)
        realite = realite[indices]
        #print(len(realite))
        #print(len(simulation))
        t = np.arange(len(realite))

        plt.plot(t, realite, lw=2, label='real data', color='darkgreen')
        plt.plot(t, simulation, lw=2, label='real data', color='red')




    def plotValidationWithKpi1(self, burnoutLevel):
        fig = plt.figure(figsize=(50, 20))
        '''print("some sizes")
        print(len(self.__kpiRealite1))
        print(len(self.__kpisimulation1))'''

        for it in range(self.__nbCluster):
            fig.add_subplot(7,4, it+1)
            self.plotRealiteEtSimulation(self.__kpiRealite1[it][burnoutLevel], self.__kpisimulation1[it][burnoutLevel])
        plt.show()
        ##################################################
        ##################################################
##############################################################################################





    '''##############################################################################################################################################################'''

    '''#################################     PLOT DES RESULTATS EN SORTIE DE NOS REPLICATION AVEC INTERVALLE DE CONFIENCE, MOYENNE, REALITE                ##########'''

    '''##############################################################################################################################################################'''

    '''J'ai codé deux fonction pour assurer mes plots à la fin de mes réplication'''

    '''Fonction  plotErrorSimulationEtRealite : reççois pour chaque cluster : moyenne, born surp, bonr inf des résultats de réplication (le nombre d'aidant dans un état) 
     dans le vecteur simulation + UN VECTEUR realite qui suppose la realite des donneés 
         ==>> en sortie : le plot '''
    def plotErrorSimulationEtRealite(self, simulation, real):
        t = np.arange(len(simulation[0]))
        indices = np.arange(len(real) - 1)## une petite manip (je veux que les résultats soient affichés sur 119 pas de temps au lieu de 120 pas de temps)
        real = real[indices]
        plt.plot(t, simulation[0], lw=2, label='Simulation', color='red')
        plt.plot(t, real, lw=2, label='Simulation', color='green')
        plt.fill_between(t, simulation[1], simulation[2], facecolor='coral', alpha=0.5)

    '''Fonction  plotResultsReplication : organise le plot sur plusieurs cluster pour chaque cluster utiliser le fonction plotErrorSImulationEtRealite '''
    def plotResultsReplications(self, kpiReplicationSimulations, burnoutLevel):
        fig = plt.figure(figsize=(20, 40))
        for it in range(self.__nbCluster):
            fig.add_subplot(10,3,it+1)
            self.plotErrorSimulationEtRealite(kpiReplicationSimulations[burnoutLevel][it], self.__kpiRealite1[it][burnoutLevel])
        plt.show()
    '''##############################################################################################################################################################'''
    '''##############################################################################################################################################################'''
    '''##################################################################################################################################################################'''




    '''##################################################################################################################################################################'''

    '''########################################      #MISE   EN FORME DE DONNEES ET CREATION D'INTERVALLE DE CONFIANCE   ############################################'''

    '''##############################################################################################################################################################'''
    def createConfidenceIntervalle(self, clusterReplications):
        '''L'intervalle de confience seras calculé pour chaque pas de temps de ce fait :
        -- Pour chaque pas de temps on aura MOYENNE, BONRNE INF, BORNE SUP
        ---Résultats ====>>> un vecteur en trois dimentions (MOYENNE, BONRNE INF, BORNE SUP)
                ---  Pour chaque dimension ==>> un vecteur sur une dimension de pas de temps '''
        ## La structure de données à retouner
        intevalleConfience = np.zeros((3, self.__timeHorizon-1))
        ## Transposer la liste (clusterReplications), pour calculer la moyenne de réplication en fonction de son pas de temps

        for index , it in enumerate(clusterReplications.T):
            intevalleConfience[0][index] = np.mean(it) ## la moyenne occupe la position 0 dans notre vecteur
            t_std = stats.t.ppf(q=0.95, df=len(it) - 1)
            error = t_std * (statistics.stdev(it) / float(math.sqrt(len(it))))
            intevalleConfience[1][index] = intevalleConfience[0][index]+error ## La borne suppp occupe la position 1 dans notre vecteur
            intevalleConfience[2][index] = intevalleConfience[0][index]-error ## La borne inf occupe la position 1 dans notre vecteur
        return intevalleConfience

    def trairementDonnesReplications(self):
        '''En premier on transforme les données comme suit :
        Les données de self.__kpiReplicateSimulation sont ordonée sous forme :
         sahpe[NumbRéplicaation][Cluster][nbStates][Temps] ====>> Transformation ====>>  Shape[nbStates][cluster][NumbReplication][Temps]'''
        # le nouveau format de données
        kpiReplicationBis = np.zeros((self.__nbrStatePerCluster, self.__nbCluster, self.__nbReplication, self.__timeHorizon-1))
        for it in range(self.__nbrStatePerCluster):
            for i in range(self.__nbCluster):
                for j in range(self.__nbReplication):
                    for k in range(self.__timeHorizon-1):
                        kpiReplicationBis[it][i][j][k] = self.__kpiReplicateSimulation[j][i][it][k]

        '''Suivant le nouveau format de données kpiReplicationBis, on procedra comme suit : 
            ---Pour chaque cluster on nbReplication ===>> on va calculer son intervalle de confience'''
        confidenceIntervallFroAllClusters = np.zeros((self.__nbrStatePerCluster, self.__nbCluster, 3, self.__timeHorizon-1))
        for it in range(self.__nbrStatePerCluster):
            for i in range(self.__nbCluster):
                confidenceIntervallFroAllClusters[it][i] = self.createConfidenceIntervalle(kpiReplicationBis[it][i])
        return confidenceIntervallFroAllClusters
    '''##############################################################################################################################################################'''
    '''##############################################################################################################################################################'''
    '''##################################################################################################################################################################'''



    #Foncrion pour simuler le system avec intervention de l'équipe Mobile
    def simulate(self):
        for time in range(self.__timeHorizon-1):###Boucler sur le temps de simultion (durée de l'enquette et collecte de données)
#        for time in range(10):
            '''print("###########Itération Num  :  " + str(time+1) + "#################################################")
            print("#################################################################################################")
            print(self.printToCheck())
            print("#################################################################################################")'''

#            for clus in range(1):
            for clus in range(self.__nbCluster):###Boucler sur les cluster (classe) d'aidants
#                for car in range(5):
                for car in range(self.__nbCaregiversPerCluster):#Boucler suir les aidants(caregiver) d'un cluster
                    caregiverTemp = self.__matrixOfCaregivers[clus][car]

                    ## on va prendre l'évalution du Kpi pour chaque aidant à chaque pas de temps
                    burnoutLevel = int(caregiverTemp.getBurnout()-1)
                    #if (burnoutLevel == 4):
                     #   print("c 'est ici")
                    #print("on préléve l'épuisement !!!!!")
                    #print(burnoutLevel)
                    self.__kpisimulation1[clus][burnoutLevel][time]+=1
                    ############################################################################
                    if caregiverTemp.getInrespite() == 1:# si l'aidant est en service de répit
                        if caregiverTemp.getDurationOfRespite() > 0: ## si la durée de soins n'est pas fini alors décrementer
                            caregiverTemp.decrementerDureeRepit()
                            if caregiverTemp.getDurationOfRespite() == 0:## on re-verifie si la durée de soin de répit est fini !  Si oui ? alors
                                caregiverTemp.quitterServiceRepit()  ## le caregiver (aidant) va quitter le service de répit
                                #self.traiterFileAttenteCaregivers()  ## quand l'aidant (caregivger) quitte le service de répit alors un lit(ressource) se libère ne maison de répit et il faut admetre un autre aidant de ma fille d'attente du service en question
                    ##elif caregiverTemp.enAttenteEquipeMobile
                    elif caregiverTemp.getInrespite() == 0 :# si l'aidant n'est pas en attente d un service de répit &&& n'est âs en attente d'une inteventuion d l'équipe mobile:
                        valrand = np.random.randint(1,10)/10## variable aléatoire pour une prise en chrage de l'équipe mobile à un aidant (caregiver)
                        if valrand < self.__inpuData.getFrequenceRespit(): # Si Oui
                            caregiverTemp.prendreSoinsDeRepit()  ## l'aidant (caregiver) va demander les soins de répit
                        else:
                            self.__populationOfCaregivers.updateStateCaregiver(clus, car,caregiverTemp.getDurationWithoutRespite(),caregiverTemp)  # l'aidant continue son évolution directement
                            caregiverTemp.incrementerDureeSansRepit()  # incrémenter la duréé passeé dans soins de répit pour un aidant (caregiver)
                    else:#Si non
                        #print("voila le temps passé sans soins de répit  : " + str(caregiverTemp.getDurationWithoutRespite()))
                        self.__populationOfCaregivers.updateStateCaregiver(clus, car, caregiverTemp.getDurationWithoutRespite(), caregiverTemp)#l'aidant continue son évolution directement
                        caregiverTemp.incrementerDureeSansRepit()# incrémenter la duréé passeé dans soins de répit pour un aidant (caregiver)

        #self.getKpiInRealite()  # évaluer KPI selon la réalité (sur les données collectées)
        #self.plotValidationWithKpi1(3)


        def simulateAvecPrediction(self):
            for time in range(
                    self.__timeHorizon - 1):  ###Boucler sur le temps de simultion (durée de l'enquette et collecte de données)
                #        for time in range(10):
                '''print("###########Itération Num  :  " + str(time+1) + "#################################################")
                print("#################################################################################################")
                print(self.printToCheck())
                print("#################################################################################################")'''

                #            for clus in range(1):
                for clus in range(self.__nbCluster):  ###Boucler sur les cluster (classe) d'aidants
                    #                for car in range(5):
                    for car in range(self.__nbCaregiversPerCluster):  # Boucler suir les aidants(caregiver) d'un cluster
                        caregiverTemp = self.__matrixOfCaregivers[clus][car]

                        ## on va prendre l'évalution du Kpi pour chaque aidant à chaque pas de temps
                        burnoutLevel = int(caregiverTemp.getBurnout() - 1)
                        # if (burnoutLevel == 4):
                        #   print("c 'est ici")
                        # print("on préléve l'épuisement !!!!!")
                        # print(burnoutLevel)
                        self.__kpisimulation1[clus][burnoutLevel][time] += 1
                        ############################################################################
                        if caregiverTemp.getInrespite() == 1:  # si l'aidant est en service de répit
                            if caregiverTemp.getDurationOfRespite() > 0:  ## si la durée de soins n'est pas fini alors décrementer
                                caregiverTemp.decrementerDureeRepit()
                                if caregiverTemp.getDurationOfRespite() == 0:  ## on re-verifie si la durée de soin de répit est fini !  Si oui ? alors
                                    caregiverTemp.quitterServiceRepit()  ## le caregiver (aidant) va quitter le service de répit
                                    # self.traiterFileAttenteCaregivers()  ## quand l'aidant (caregivger) quitte le service de répit alors un lit(ressource) se libère ne maison de répit et il faut admetre un autre aidant de ma fille d'attente du service en question
                        ##elif caregiverTemp.enAttenteEquipeMobile
                        elif caregiverTemp.getInrespite() == 0:  # si l'aidant n'est pas en attente d un service de répit &&& n'est âs en attente d'une inteventuion d l'équipe mobile:
                            valrand = np.random.randint(1,10) / 10  ## variable aléatoire pour une prise en chrage de l'équipe mobile à un aidant (caregiver)
                            if valrand < self.__inpuData.getFrequenceRespit():  # Si Oui
                                caregiverTemp.prendreSoinsDeRepit()  ## l'aidant (caregiver) va demander les soins de répit
                            else:
                                self.__populationOfCaregivers.updateStateCaregiver(clus, car,caregiverTemp.getDurationWithoutRespite(),caregiverTemp)  # l'aidant continue son évolution directement
                                caregiverTemp.incrementerDureeSansRepit()  # incrémenter la duréé passeé dans soins de répit pour un aidant (caregiver)
                        else:  # Si non
                            # print("voila le temps passé sans soins de répit  : " + str(caregiverTemp.getDurationWithoutRespite()))
                            self.__populationOfCaregivers.updateStateCaregiver(clus, car,caregiverTemp.getDurationWithoutRespite(),caregiverTemp)  # l'aidant continue son évolution directement
                            caregiverTemp.incrementerDureeSansRepit()  # incrémenter la duréé passeé dans soins de répit pour un aidant (caregiver)

            # self.getKpiInRealite()  # évaluer KPI selon la réalité (sur les données collectées)
            # self.plotValidationWithKpi1(3)

    def replicateSimulation(self):
        for it in range(self.__nbReplication):
            self.simulate()
            self.__kpiReplicateSimulation.append(self.__kpisimulation1)

            del(self.__matrixOfCaregivers, self.__kpisimulation1)
            self.__matrixOfCaregivers = copy.deepcopy(self.__populationOfCaregivers.getMatrixOfCaregivers())
            self.__kpisimulation1 = np.zeros((self.__nbCluster, self.__nbrStatePerCluster, self.__timeHorizon - 1))
        self.getKpiInRealite()
        listErrorIntervallToPlot = self.trairementDonnesReplications()
        self.plotResultsReplications(listErrorIntervallToPlot, 3)






    def printToCheck(self):

        for i in range(5):
            print('*'*33)
            print(self.__matrixOfCaregivers[0][i])





    def __repr__(self):
        return " La classe Simulation comporte: nbCluster({}), nbCaregiverPerCluster({}), nbStatesPerCluster({}), timeHorizon({}) nbReplication({})".format(self.__nbCluster, self.__nbCaregiversPerCluster, self.__nbrStatePerCluster,
                                                                                          self.__timeHorizon, self.__nbReplication)



