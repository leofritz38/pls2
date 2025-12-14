#interpret_data

from data_loading import file_downloader
import models
import optimizer
import distances
import numpy 
from sys import argv
import matplotlib.pyplot as plt
from models import Model2 # to be removed may be
import pandas

# ---------------data downloading-----------
file_nameT=argv[1]
data_algea=file_downloader(file_name=file_nameT)

# -----------------------data exploitation with some MODELs and some DISTANCES computing
used_dist=["least_square_distance","least_square_distance2"]

optimized_parameters=optimizer.optimize_models(modname=["Model1","Model2"],dist=used_dist,rawdata=data_algea) 
best_optimization_per_distance=optimizer.get_best_prediction(optimized_parameters)
print(best_optimization_per_distance)
# print(optimized_parameters)
# plot it now---------------------------------------------------
# Extraire ETRmax et alpa
ETRmax =float(optimized_parameters['Model2']['least_square_distance']['optimized_parameters']['ETRmax'])
alpha = float(optimized_parameters['Model2']['least_square_distance']['optimized_parameters']['alpha']) 

print(alpha, "alpha")
print(type(alpha), "alpha type")
rETR_easy=data_algea["rETR"].values
E=data_algea["PAR"].values


parameters = [ ETRmax, alpha]
rETR_model=Model2(E,param=parameters)
print(rETR_model[:10], "les 5 premières valeurs de rETR_model")
print(rETR_easy[:10], "les 5 premières valeurs de rETR_easy")

# # firugre -----------------------------------
# plt.figure()  # Crée une nouvelle figure vide
# plt.plot(rETR_easy, rETR_model )  #
# plt.xlabel('ETR from simpler model')
# plt.ylabel('ETR from model to get coefficient')
# plt.title('peformance du meilleur modèle a reproduire les données')
# plt.grid(True)
# plt.show()


# --------------representer alpha en fonction du temps ? -----------
# creer element pour la figure de alpha en fonction du temps et alpha en fonction du ph 
# obtenir alpha 
# travaillans colomne par colomne 
# ajoute un colomne   alpha
alphas = []
window_size = 5

window_data=data_algea.iloc[0:30] # ligne ou colomne
print(window_data, " premier lignes toutes les colomnes ? ")

result = optimizer.optimize_models(
        modname=["Model2"],
        dist=used_dist,
        rawdata=window_data
    )

alpha=result['Model2']['least_square_distance']['optimized_parameters']['alpha']
print(alpha, " alpha singulier")
alphas.append(alpha)
print(alphas , "vecteur alphaS")
print(Model2(E=window_data["PAR"].values, param=[ETRmax,alpha]), "rETR estimé pour un alpha local d 'une fenetre de 5 ")

# for i in range(len(data_algea)):
#     # Prendre 5 lignes autour de la ligne i
#     start = max(0, i - window_size//2)
#     end = min(len(data_algea), i + window_size//2 + 1)
    
#     window_data = data_algea.iloc[start:end]
    
#     result = optimizer.optimize_models(
#         modname=["Model2"],
#         dist=used_dist,
#         rawdata=window_data
#     )
    
#     alpha = result['Model2']['least_square_distance']['optimized_parameters']['alpha']
#     alphas.append(alpha)

# data_algea['alpha'] = alphas

# X=data_algea["t in s"].values
# Y=data_algea["alpha"].values
# # firugre -----------------------------------
# plt.figure()  # Crée une nouvelle figure vide
# plt.plot(X,Y, marker='o')  #
# plt.xlabel('ETR from simpler model')
# plt.ylabel('ETR from model to get coefficient')
# plt.title('peformance du meilleur modèle a reproduire les données')
# plt.grid(True)
# plt.show()


#pb dans le run le run ne s'arrepe pas, faut commencer par calculer un alpha ? 