print("Hello c'est mon nouveau programme ici .....")

import pandas as pd
import numpy as np




import InputData
import PopulationCaregiver
import Simulation
import ServiceOfRespite




inputData = InputData.InputData()
inputData.importData()

#print(inputData.getMarkovMatrix())
serviceRepit = ServiceOfRespite.ServiceOfRespite(inputData)




populationCaregivers = PopulationCaregiver.PopulationCaregiver(inputData, serviceRepit)
populationCaregivers.importData()


populationCaregivers.generatePopulation()

populationCaregivers.printTableCaregivers()


simulation = Simulation.Simulation(inputData, populationCaregivers, serviceRepit)
#simulation.simulate()
simulation.replicateSimulation()
