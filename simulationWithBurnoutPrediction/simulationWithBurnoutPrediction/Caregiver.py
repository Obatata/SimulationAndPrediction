# -*- coding: utf-8 -*-
"""
Created on Mon Octobre 1 10:34:24 2018

@author: Oussama BATATA
"""
import numpy as np

class Caregiver:
    """Classe définiss un aidant (caregiver) caractérisée par :

    - id = pour réferencier notre aidant

    - burnout  = son niveau d'épuisemen ("burnout" & "No burnout") == > (0, 1)

    - inRespitee = son statut de répit ("en répit"  & "n'est pas en répit") ==>  (0, 1)

    - durationWithoutRespite = Sa duréee sans soins de répit ;

    - durationOfRespite = Sa durée de répit si il est pris en charge par un service de répit

    - inHospital = Son statut envers l'hôîtal si il est a ("hospitalisé son aidant" ou "non") ==> (0,1)

    - durationInHospital =  La durée d'hospitalisation si l'a a fait à son patient"""




    def __init__(self,  idCaregiver, idCluster, idInCluster, burnout, serviceRepit):  # Notre méthode constructeur

        """Constructeur de notre classe. Chaque attribut va être instancié

        avec une valeur par défaut..."""

        """À chaque fois qu'on crée un objet, on incrémente l' id"""


        self.__idCaregiver = idCaregiver

        self.__idCluster = idCluster

        self.__idInCluster = idInCluster

        self.__burnout = burnout

        self.__SEUILBURNOUTURGENCE = 3
        ########################################################################################
        ##########################################################################################
        ######################################################################################
        '''Attributs qui font référence à la situation de l'aidant envers les services de répit'''



        self.__inRespite = 0  # à leurs création les aidant ne sont pas pris en charge par des soins de répit


        ##############################################################
        self.__inHospital = 0 # dans l'hôpital ou non
        ##############################################################


        ##############################################################
        self.__inRespitServiceQue = 0  #  l'aidant est en attente pour un service de répit
        ##############################################################

        ################################################################


        ################################################################


        self.__durationWithoutRespite = 0  # // dureé passé sans soins de répit

        self.__durationOfRespite = 0  # //  duréee de répit si le caregiver est assigné à un service de répit

        self.__inWaitRespite = 0  # //  dirée passé dans une fille d'attente pour le caregiver

        self.__inHospital = 0  # à leurs création les aidant n'hospitalisent pas leurs aidants

        self.__durationInHospital = 0  # //  duréee d'hospitalisation du caregiver pour son patient

        self.__serviceRepit = serviceRepit  # // Le service de répit dans lequel sera assigné notre aidant (caregiver) pour prendre des soins de répit



    '''''---------------------Mes fonctions get -----------------------------------------'''

    #self.__idCaregiver
    def getIdCaregiver(self):
        return self.__idCaregiver

    #self.__idCluster
    def getIdCluster(self):
        return self.__idCluster


    #self.__idInCluster
    def getIdInCluster(self):
        return self.__idInCluster


    #self.__burnout
    def getBurnout(self):
        return self.__burnout

        ########################################################################################
        ##########################################################################################
        ######################################################################################


    #self.__idInRespitequeue
    def getInRespiteServiceQue(self):
        return self.__inRespitServiceQue



    #self.__inRespite
    def getInrespite(self):
        return self.__inRespite

    #self.__durationWithoutRespite
    def getDurationWithoutRespite(self):
        return self.__durationWithoutRespite


    #self.__durationOfRespite
    def getDurationOfRespite(self):
        return self.__durationOfRespite

    #self.__inWaitRespite
    def getInWaitRespite(self):
        return self.__inWaitRespite

    #self.__inHospital
    def getInHospital(self):
        return self.__inHospital

    #self.__durationInHospital
    def getDurationinHospital(self):
        return self.__durationInHospital




    ''''---------------------------------------------------Fuin des fonction de get ----------------------------------------'''''
    '''''---------------------Mes fonctions set -----------------------------------------'''
    #self.__burnout
    def setBurnout(self, burnoutLevel):
        self.__burnout = burnoutLevel



    def setInRespite(self, inRespite):
        self.__inRespite = inRespite


    def setInWaitRespite(self, inWaitRespite):
        self.__inWaitRespite = inWaitRespite

    #self.__durationOfRespite
    def setDurationOfRespite(self, durationOfRespite):
        self.__durationOfRespite = durationOfRespite


    '''############################################################'''
    '''############################################################'''
    '''Set parameter of service de répit '''

    def setInRespiteServiceQue(self, inRespiteServiceQue):
        self.__inRespitServiceQue = inRespiteServiceQue

    '''############################################################'''
    '''############################################################'''



    '''############################################################'''
    '''############################################################'''
    '''Set parameter of respite home '''

    def setInrespiteHome(self, inRespiteHome):
        self.__inRespiteHome = inRespiteHome

    def setInRespiteHomeQue(self, inRespiteHomeQue):
        self.__inRespiteHomeQue = inRespiteHomeQue


    '''############################################################'''
    '''############################################################'''

    #self.__inWaitRespite

    #self.__dureeAttenteEquipeMobile
    def setDureeAttenteEquipeMobole(self, dureeeAttenteEquipeMobile):
        self.__dureeAttenteEquipeMobile = dureeeAttenteEquipeMobile

    def setListeIntevenantEquipeMobile(self, indiceIntervenant):
         self.__listeIntervenantEquipeMobile.append(indiceIntervenant)

    def libereIntevenantEquipeMobile(self):
        del self.__listeIntervenantEquipeMobile[:]


    def decrementerDureeRepit(self):
        self.__durationOfRespite-=1


    def incrementerDureeSansRepit(self):
        self.__durationWithoutRespite+=1





    def prendreSoinsDeRepit(self):

        '''print("checker  file d'attente dans class caregiver")
        print(self.__serviceRepit.fileAtteteCaregivers)
        print("resources répit : " +str(self.__serviceRepit.nbLitsDispo))'''

        if self.__serviceRepit.getNbLitsDispoRespiteService() > 0 and not self.__serviceRepit.getFilleAtteteRespiteService():## Si des lits sont dispo au service de répit  &   la liste d'attente des aidants est vide
            self.__inRespite = 1
            self.__serviceRepit.decrementerNumberLitsServiceRepit()
            self.__inWaitRespite = 0
            self.__durationOfRespite = self.__serviceRepit.getDureeInServiceRepit()
            self.__inRespitServiceQue = 0
        else:
            '''print("rjoindre la file d'attente avec l'id :")
            print(self.__idCaregiver)'''
            self.__serviceRepit.ajouterCaregiverDansFilleAttenteRespiteService(self)
            self.__inWaitRespite = 1
            self.__inRespitServiceQue = 1

    def prendreSoinsDeRepiAvecPrediction(self):

        '''print("checker  file d'attente dans class caregiver")
        print(self.__serviceRepit.fileAtteteCaregivers)
        print("resources répit : " +str(self.__serviceRepit.nbLitsDispo))'''
        nextBurnoutState = np.random.randint(1,5)

        if self.__serviceRepit.getNbLitsDispoRespiteService() > 0 and not self.__serviceRepit.getFilleAtteteRespiteService() and nextBurnoutState > self.__SEUILBURNOUTURGENCE:  ## Si des lits sont dispo au service de répit  &   la liste d'attente des aidants est vide
            self.__inRespite = 1
            self.__serviceRepit.decrementerNumberLitsServiceRepit()
            self.__inWaitRespite = 0
            self.__durationOfRespite = self.__serviceRepit.getDureeInServiceRepit()
            self.__inRespitServiceQue = 0
        else:
            '''print("rjoindre la file d'attente avec l'id :")
            print(self.__idCaregiver)'''

            self.__serviceRepit.ajouterCaregiverDansFilleAttenteRespiteService(self)
            self.__inWaitRespite = 1
            self.__inRespitServiceQue = 1

    def quitterServiceRepit(self):
        self.__inRespite = 0
        self.__durationOfRespite = 0
        self.__durationWithoutRespite = 0
        self.__inWaitRespite = 0
        self.__serviceRepit.incrementerNumbreLitsServiceRepit()
        benefice = self.__serviceRepit.getBeneficeRespiteService()

        self.__serviceRepit.predreRepitDeFilleAttente()

        self.__burnout -= benefice

        if self.__burnout < 1:
            self.__burnout = 1
        elif self.__burnout > 5:
            self.__burnout = 5

        #print("mon épuisement apres le service de répit est comme suit : " + str(self.__burnout))



    def __str__(self):
        """Quand on entre notre objet aidant dans l'interpréteur"""
        return " idCluster({}), idInCluster({}),  burnout({}), inWaitRespite({}), inRespiteServiceQue({}), inRespite({}), dureeRespite({}), inHospital({}), durationHosîtal({}), withoutRespite({}))".format(
            self.__idCluster, self.__idInCluster, self.__burnout, self.__inWaitRespite, self.__inRespitServiceQue, self.__inRespite, self.__durationOfRespite,
            self.__inHospital, self.__durationInHospital, self.__durationWithoutRespite)
