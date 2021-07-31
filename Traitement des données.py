import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

clear = lambda: os.system('cls')
clear()

#Folder to edit to your specific location
FolderLocation="Data"

#âth to files
items = os.listdir(FolderLocation)

# Récupération de tous les CSV dans une liste
CSVList = [pd.read_csv(FolderLocation+"\\"+name, header=None) for name in items if name.endswith(".csv")]

#empty DF
DF = pd.DataFrame()

#adding all csv files which containing one column data
DF["Consommation électrique"]=-CSVList[0][0]
DF["Consommation thermique"]=-CSVList[1][0]
DF["Production électrique"]=CSVList[2][0]

#Listing all 
F = [name for name in items if name.endswith(".npy")]

#.npy -> list of array
res = [np.load(FolderLocation+"\\"+name, allow_pickle=True) for name in items if name.endswith(".npy")]

#file to post treat
Fichier = 2
print("Fichier : ",F[Fichier])

#Copying
res2 = res[Fichier].copy()
Conso_Elec_post = res2[3].copy()
Conso_Ther_post = res2[4].copy()
Prod_Elec_post = res2[3].copy()

#Conditionning data
for i in range(len(Conso_Elec_post)):
    if Conso_Elec_post[i]>0:
        Conso_Elec_post[i]=0
    if Conso_Ther_post[i]>0:
        Conso_Ther_post[i]=0
    if Prod_Elec_post[i]<0:
        Prod_Elec_post[i] = 0
            
#adding some new columns
DF['Consommation électrique non satisfaite']=Conso_Elec_post
DF['Consommation thermique non satisfaite']=Conso_Ther_post
DF['Production électrique non utilisée']=Prod_Elec_post
DF['Commande du stockage']=res2[13]
DF['Etat de charge du stockage']=res2[15][:-1]
DF['Commande du P2H']=res2[10]
DF['Commande du H2P']=res2[11]

#plotting
col= ['#098CB6','#C10244', 'g','#C10244','tab:cyan','tab:orange','#C10244','#C10244']

t = [i for i in range(8760)]
fig, axs = plt.subplots(4, 1)
j = 0
linewidth=1
for i in [DF['Consommation électrique'], DF['Consommation thermique'], DF['Production électrique']]:
    axs[0].plot(t, i,  label=i.name,  drawstyle='steps-post', color=col[j],lw=linewidth)
    j=j+1
    
axs[0].set_ylim(-3,8)
axs[0].legend(ncol=3)
axs[0].set_xlim(1000,2000)
axs[0].set_ylabel('Puissance [MW]')
j = 0
for i in [DF['Consommation électrique non satisfaite'], DF['Consommation thermique non satisfaite'], DF['Production électrique non utilisée']]:
    axs[1].plot(t, i, label=i.name,  drawstyle='steps-post', color=col[j],lw=linewidth)
    j=j+1

axs[1].set_ylim(-3,8)
axs[1].legend(ncol=3)
axs[1].set_xlim(1000,2000)
axs[1].set_ylabel('Puissance [MW]')

j = 0
for i in [DF['Commande du stockage'],DF['Commande du P2H'],DF['Commande du H2P']]:
    axs[2].plot(t, i, label=i.name,  drawstyle='steps-post', color=col[j+3],lw=linewidth)
    j=j+1

axs[2].set_xlim(1000,2000)
axs[2].set_ylim(-3,8)
axs[2].legend(ncol=3)
axs[2].set_ylabel('Puissance [MW]')

axs[3].plot(t,DF['Etat de charge du stockage'], label="Etat de charge du stockage", drawstyle='steps-post',color=col[-1],lw=linewidth)
axs[3].legend(ncol=3)
axs[3].set_xlim(1000,2000)
axs[3].set_ylabel('Energie [MWh]')
axs[3].set_xlabel('Temps [h]')


axs[0].grid()
axs[1].grid()
axs[2].grid()
axs[3].grid()

plt.show()

# Percentage
print("Pourcentage de la production renouvelable utilisé localement (synchronisé) : ", round(1-DF['Production électrique non utilisée'].sum(axis=0)/DF['Production électrique'].sum(axis=0),2))

print("Taux de satisfaction des besoins électrique par du renouvelable : ", round(1-DF['Consommation électrique non satisfaite'].sum(axis=0)/DF['Consommation électrique'].sum(axis=0),2))

print("Taux de satisfaction des besoins thermique par du renouvelable : ",round(1-DF['Consommation thermique non satisfaite'].sum(axis=0)/DF['Consommation thermique'].sum(axis=0),2))



