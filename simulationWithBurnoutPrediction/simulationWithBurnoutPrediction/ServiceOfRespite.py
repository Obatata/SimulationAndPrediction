# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:34:24 2018

@author: Oussama BATATA
"""
import numpy as np
import collections


import InputData


class ServiceOfRespite:
    """Classe définiss un aidant (caregiver) caractérisée par :

    - id = pour réferencier le service de répit en question

    - typeService   = type du service

    - nbLits = nombre de lits

    - nblitsDispo = nb de lits dispo

    - fileAttenteAIdants = les aidans en file d'attente pour ce service de répit

    """






    def __init__(self, inputData):  # Notre méthode constructeur

        ## attributs pour acceder à la classe inputData
        self.__inpuData = inputData


        '''Les attributs d'un service de répit ordinaire'''
        self.__NBRLITSRESPITESERVICE = 20*101
        self.__nbrLitsDispoRespiteService = self.__NBRLITSRESPITESERVICE
        self.__nbrLitsOccupeRespiteService = 0
        self.__fileAtteteRespiteService = collections.deque([])





        '''Les attributs de l'hopital '''
        self.__nbrLitsOccupeHospital = 0






    ''' VOici mes fonction pour geter les attributs de ma class '''



    def predreRepitDeFilleAttente(self):

        if  self.__fileAtteteRespiteService:
            caregiver = self.__fileAtteteRespiteService[len(self.__fileAtteteRespiteService) - 1]
            caregiver.setInRespite(1)
            caregiver.setInWaitRespite(0)
            caregiver.setDurationOfRespite(self.getDureeInServiceRepit())
            caregiver.setInRespiteServiceQue(0)
            self.decrementerNumberLitsServiceRepit()
            self.__fileAtteteRespiteService.pop()



    '''Les fonction spéciphique pour mon service de répit '''
    '''########################################################################'''

    '''####################   SERVICE DE REPIT     #######################'''

    '''########################################################################'''
    def ajouterCaregiverDansFilleAttenteRespiteService(self, idCaregiver):
        self.__fileAtteteRespiteService.appendleft(idCaregiver)

    def getDureeInServiceRepit(self):
        tempsRepit = np.random.randint(1,7)
        return tempsRepit

    def decrementerNumberLitsServiceRepit(self):
        self.__nbrLitsDispoRespiteService-=1

    def incrementerNumbreLitsServiceRepit(self):
        self.__nbrLitsDispoRespiteService+=1

    def getBeneficeRespiteService(self):
        benefice = np.random.randint(4,5)
        return benefice


    #self.__nbrLitsDispoRespiteHome
    def getNbLitsDispoRespiteService(self):
        return self.__nbrLitsDispoRespiteService

    #self.__fileAtteteRespiteService
    def getFilleAtteteRespiteService(self):
        return self.__fileAtteteRespiteService
    '''########################################################################'''
    '''########################################################################'''
    '''########################################################################'''





    '''Les fonction spéciphique pour l' hôpital'''
    '''########################################################################'''

    '''#####################     HOSPITAL           ################################'''

    '''########################################################################'''

    def getDureeInHospital(self):
        tempsRepit = np.random.randint(1, 7)
        return tempsRepit


    def getBeneficeHospital(self):
        benefice = np.random.randint(4, 5)
        return benefice

    '''########################################################################'''
    '''########################################################################'''
    '''########################################################################'''

    def __repr__(self):
        """Cmlasse service de répit :"""
        return "Voila la classe de service de répit :   id du service de répit ({}), type du service de répit({}), nombre de lit dispo ({}), la fille d'attente des aiadnts ({}]".format(self.__id, self.__typeService, self.__nbrLitsDispoRespiteService, self.__fileAtteteRespiteService)
