#interpret_data


import models
import optimizer
import distances
import numpy 
from sys import argv
import matplotlib.pyplot as plt
from models import Model2 # to be removed may be
import pandas



def file_downloader(file_name):
    data=pandas.read_csv(file_name, sep=";", decimal=".")
    # print(data.head(), "all the data files")
    data_interst=data.loc[:,["t in s","PAR","ETR","rETR","F","Fm'","Y(II)"]] 
    print(data_interst.head(),"only the data of interest")
    
    return (data_interst)

# ---------------data downloading-----------
file_nameT=argv[1] # donner dans la batch de commande le nom et le paths pour acceder au donnée
data_algea=file_downloader(file_name=file_nameT) # utiliser la fonction qui prend le csv en donnée et donnes un dataframe en sortie

# -----------------------data exploitation with some MODELs and some DISTANCES computing
used_dist=["least_square_distance","least_square_distance2"] # selection des distances utilisé pour l'optimisagtion

optimized_parameters=optimizer.optimize_models(modname=["Model1","Model2"],dist=used_dist,rawdata=data_algea) # donne les paramètre optimisé sur tous les jeux de données
# quand la fonction optimizer etait construire pour obtenir des parameter sur tout le jeux de données . On s'est rendu compte plustard que la structrue du jeux de données
#etait : un individus stat egal 10 mesures
best_optimization_per_distance=optimizer.get_best_prediction(optimized_parameters) #  fonction qui avec les paramètres optimisé donnes le meilleurs modèle pour cahque distance selectioné 
print(best_optimization_per_distance) # affiche le meilleur modèle avec la distances moyennes associé ? lorsque la structure des données n'etais pas prise en compte par optimizer
# les ecart entre predictions et mesure etait tres grand 
# print(optimized_parameters)
# plot it now---------------------------------------------------
# Extraire ETRmax et alpa
ETRmax =float(optimized_parameters['Model2']['least_square_distance']['optimized_parameters']['ETRmax']) # recurper les paramètres optimisé pour le modèle 2
alpha = float(optimized_parameters['Model2']['least_square_distance']['optimized_parameters']['alpha']) 

print(alpha, "alpha")  # afficher le paramètre de croissance pour voir si il etait coherent, av prise en compte de la structure des données il ne l'etait pas


rETR_easy=data_algea["rETR"].values # recuprere les données qui doivent etre simulé par modèle 2
E=data_algea["PAR"].values # recuprer le X a mettre dans notrmodèle2 qui avec les paramètre nous renvoie notre Y : rETR


parameters = [ ETRmax, alpha] # paramètre precedement extrait de optimizer
rETR_model=Model2(E,param=parameters) # compute rETr modèle 2

print(rETR_model[:10], "les 5 premières valeurs de rETR_model") # visualiser les deux, encore une fois avnt la prise en compte de la structurations des donnees il y avait un grosse ecart
print(rETR_easy[:10], "les 5 premières valeurs de rETR_easy")

# firugre ----------------------------------- plot Y en fonction X : plot rETR estimé par rapport  rETR mesuré
plt.figure()  # Crée une nouvelle figure vide
plt.plot(rETR_easy, rETR_model )  #
plt.xlabel('ETR from simpler model')
plt.ylabel('ETR from model to get coefficient')
plt.title('peformance du meilleur modèle a reproduire les données')
plt.grid(True)
plt.show()


# --------------representer alpha en fonction du temps ? ----------- meme code avant mais bouvle For pour le faire sur tout le scripte
# creer element pour la figure de alpha en fonction du temps et alpha en fonction du ph 
# obtenir alpha 
# travaillans colomne par colomne  -> pas possible à partir de comment opimizer etait construit
# ajoute un colomne   alpha
alphas = [] # creer un vecteur vide
window_size = 5 # creer une fenetre de donnnes avec lesquelles les paramètres seront optimisées

window_data=data_algea.iloc[0:30] # ligne ou colomne
print(window_data, " premier lignes toutes les colomnes ? ")

result = optimizer.optimize_models(
        modname=["Model2"],
        dist=used_dist,
        rawdata=window_data
    ) # compute parameter value only for the data in the window

alpha=result['Model2']['least_square_distance']['optimized_parameters']['alpha']  # retreive paramèter value only for the modele and distance of intereste
print(alpha, " alpha singulier") # afficher la croissance pour voir si c'est coherant avec ce qu'on attends
alphas.append(alpha) # ajouter au vecteur nul

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