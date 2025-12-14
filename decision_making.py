### Goal of this file is to diagnostic according to parameter value
import optimizer
import distances
import models
import numpy as np
import pandas as pd


def decision_making(data,models,distances,merge_dist=False,merge_only=False,ponderation=[0.5,0.5]):
    if merge_dist and not(merge_only):
        distances.append("merge."+".".join(distances))
    if merge_only:
        distances=["merge."+".".join(distances)]
    # rawdata=data_loading.load(path)
    raw_data=data
    optimized_parameters=optimizer.optimize_models(models,distances,data,ponderation)
    best_optimization_per_distance=optimizer.get_best_prediction(optimized_parameters)
    average_best_model=[value[0] for key,value in best_optimization_per_distance.items()]
    best_opt_param={",".join([key,value[0]]): optimized_parameters[value[0]][key]["optimized_parameters"] for key,value in best_optimization_per_distance.items()}
    return best_opt_param,best_optimization_per_distance
    # if np.all(average_best_model == average_best_model[0]):
    #     #Extraire les paramètres et conclure en précisant bien que toutes les distances convergent vers le même modèle
    #     #Choisir la dist la plus petite pour le modèle
    #     #recréer le chemin (modele, puis dist) pour récupérer les paramètres
    #     # Interpréter mécaniquement les paramètres et réponse --> table de décision plutôt que if elif pitié

    # else:
    #     best_model = max(set(average_best_model), key=average_best_model.count)
    #     # Extraire et conclure sur ce dit modèle
    #     #Choisir la dist la plus petite pour le modèle majoritaire
    #     #recréer le chemin (modele, puis dist) pour récupérer les paramètres
    #     # Interpréter mécaniquement les paramètres et réponse --> table de décision plutôt que if elif pitié

# df=pd.read_csv("C:/Users/Nitro/Downloads/data/data/Online PAM/00_process_data/00_rlc_data/00_5s/00_pam1/data_PAM_LR_070_G1_MI5_MEA10_5s_PAM1.csv", sep=";", decimal=".")
# print(data.head(), "all the data files")
# data_interst=data.loc[:,["PAR","ETR","rETR","F","Fm'","Y(II)"]]
# print(data_interst.head(),"only the data of interest")
# print(decision_making(df,["Model1","Model2","Model3","Model6"],["least_square_distance_ETR","least_square_distance_median"],merge_dist=True,merge_only=False,ponderation=[0.5,0.5]))
