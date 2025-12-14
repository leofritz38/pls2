#### Ce fichier n'est pas généralisable en cas de changement de référentiel (nécessite E et rETR en valeur de x et y_ref) mais peu servir de référence pour généralisation
import pandas as pd
import numpy as np  
from sys import argv
import matplotlib.pyplot as plt
import models
import optimizer

# print("data need to be extracted fom file.zip in order ot be readen by read_csv")
# print(" give the data_file pathway with / not \ ")
# file_name=argv[1]
# #file_name="data_algae/Online_PAM/00_process_data/00_rlc_data/00_5s/00_pam1/data_PAM_LR_070_batch_G1_MI5_MEA10_5s_PAM1.csv"

# df=pd.read_csv("C:/Users/Nitro/Downloads/data/data/Online PAM/00_process_data/00_rlc_data/00_5s/00_pam1/data_PAM_LR_070_G1_MI5_MEA10_5s_PAM1.csv", sep=";", decimal=".")


# data=pandas.read_csv(file_name, sep=";", decimal=".")
# print(data.head(), "all the data files")
# data_interst=data.loc[:,["PAR","ETR","rETR","F","Fm'","Y(II)"]]
# print(data_interst.head(),"only the data of interest")
def create_fig(Path,data_proportion,model_used,dist,figname,merge_dist=False,merge_only=False,ponderation=[0.5,0.5]):
    # Lecture du fichier
    df=pd.read_csv(Path, sep=";", decimal=".")
    # Ajustement des valeurs manquantes (dans notre jeu de donnée "-")
    df.replace("-", np.nan, inplace=True)
    # Sécurité 
    df["PAR"] = pd.to_numeric(df["PAR"], errors='coerce')
    df["rETR"] = pd.to_numeric(df["rETR"], errors='coerce')
    # On enlève tous les Nas
    df_clean = df.dropna(subset=["PAR","ETR","rETR"])
    # Initialisation des séquences de résultats
    alpha={i:[] for i in dist}
    ETRmax={i:[] for i in dist}
    predicted={i:[] for i in dist}
    # Définition de la plage de mesure (par 10 car périodicité par 10 dans nos données)
    time_seq=range(10,data_proportion,10)
    # Initialisation du suivi de simulation
    percent=0.01
    # Parcours de la séquence temporelle
    for i in time_seq:
        # Optimisation des paramètres sur la séquences donné, récupération du meilleur modèle
        best_param,bestmodel=optimizer.Simulate(df.iloc[i-10:i],model_used,dist,merge_dist=merge_dist,merge_only=merge_only,ponderation=ponderation)
        # Récupération des chemins (ici pas nécessaire car on utilise finalement qu'une seule fonction)
        paths=[[key,value[0]] for key,value in bestmodel.items()]
        # On parcours les différentes distances (toujours un modèle par distance)
        for path in paths:
            # On récupère les valeurs de paramètres et on simule des données sur la plage de mesure
            key=",".join(path)
            full_param=best_param[key]
            param=[value for key,value in full_param.items()]
            alpha[path[0]]+=[param[0]]
            ETRmax[path[0]]+=[param[1]]
            model=getattr(models,path[1])
            predicted[path[0]]+=list(model(df["PAR"][i-10:i],param))
        # Suivi de simulation
        if i/time_seq[len(time_seq)-1]>percent:
           print(percent,"% simulation done")
           percent+=0.01
    # Graphique de alpha au cours du temps
    for key,value in alpha.items():
        plt.title("alpha")
        plt.scatter(time_seq,value,s=2)
        plt.savefig(figname+"alpha"+key+".png")
        plt.show()
    # Graphique de ETRmax au cours du temps
    for key,value in ETRmax.items():
        plt.title(path[1])
        plt.ylim(0, 800) 
        plt.scatter(time_seq,value,s=2)
        plt.savefig(figname+"ETRmax"+key+".png")
        plt.show()
    # Graphique de predicted vs fitted 
    for key,value in predicted.items(): 
        print(len(value))  
        plt.title(key)
        plt.scatter(df["rETR"][:data_proportion-1],value,color="red")
        plt.savefig(figname+"predicted_vs_fitted"+key+".png")
        plt.show()
    return ("Done")
# Définition des paramètres et execution de la fonction
# La simulation peut être longue, il est recommandé de tester avec une seul distance et un seul modèle, voir de réduire la plage temporelle
PATH="C:/Users/Nitro/Downloads/data/data/Online PAM/00_process_data/00_rlc_data/00_10s/01_pam3/data_PAM_LR_070_G1_MI5_MEA10_10s_PAM3.csv"
dist=["least_square_distance_ETR"]
model_used=["Model2","Model3","Model6"]
figname="Pam3_10s_test_multi_mod"
data_proportion=120001 
### Warning : data_propotion modulo 10=1 étant donné la périodicité de nos données, sinon la dernière partie de la séquence ne sera pas traité
create_fig(PATH,data_proportion,model_used,dist,figname)