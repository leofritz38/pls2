#### Ce fichier contient toutes les fonctions nécessaires à une optimisation

import models
from scipy.optimize import minimize
import numpy as np
import inspect
import types
import distances


def optimize_models(modname,dist,rawdata,ponderation):
    ##############################
    # Cette fonction exécutent l'optimisations de toutes les combinaisons modèle distance fourni en entrée
    # les sorties s'organisent de la façon suivant : {Modele:{Dist1:{param:{},distvalue:float}}}
    ##############################
    # Premier cas de figure, plusieurs modèles qui tournent
    if isinstance(modname,list):
        # On execute la fonction sur chaque modèle individuel puis on stock le tout dans un dico de la strcture suivante :
        # {mod_name:{dist_name:{parametre_opti:list,min_dist:value}}}
        # Si une seule distance alors le dictionnaire ne contient pas de section dist_name
        multi_mod_param_opti={}
        for single_model in modname:
            multi_mod_param_opti[single_model]=optimize_models(single_model,dist,rawdata,ponderation)
        return(multi_mod_param_opti)
    elif isinstance(dist,list):
        # On execute la fonction sur chaque modèle individuellement
        multi_dist_param_opti={}
        for single_dist in dist:
            multi_dist_param_opti[single_dist]=optimize_models(modname,single_dist,rawdata,ponderation)
        return(multi_dist_param_opti)    
    elif isinstance(modname,str) and isinstance(dist,str) and dist.split(".")[0]!="merge":
        # On récupère la fonction de distance associé à la chaine de caractère
        current_dist=getattr(distances,dist)
        # On récupère le modèle associé à la chaine de caractère
        current_mod = getattr(models, modname)
        # On charge les datas 
        ##### A MODIFIER CE N'EST QUE DES FAUSSES SIMULATION UNTIL NOW
        reference_data=rawdata
        # On récupère la liste des paramètres à inférer (nom + nombre)
        list_param=inspect.signature(current_mod)
        to_opt=list(list_param.parameters.values())[1].default
        ### Definir la plage x, y et les paramètres à optimiser
        # Définition des valeurs de paramètres à priori
        prior=generate_prior(to_opt)
        # Exctraction des données nécessaires
        ### Exécuter l'optimisation et récupérer la distance
        res=minimize(current_dist,x0=prior,args=(current_mod,rawdata))
        ### Récupérer les valeurs de paramètres optimisé.
        final={}
        for i in range(len(to_opt)):
            final[to_opt[i]]=res.x[i]
        optim={}
        optim["optimized_parameters"]=final
        optim["minimal_dist"]=res.fun
        return optim
    elif isinstance(modname,str) and isinstance(dist,str) and dist.split(".")[0]=="merge":
        # On récupère la fonction de distance associé à la chaine de caractère
        dist_to_merge=dist.split(".")[1:]
        current_dist=getattr(distances,"merge_distance")
        # On récupère le modèle associé à la chaine de caractère
        current_mod = getattr(models, modname)
        # On charge les datas 
        ##### A MODIFIER CE N'EST QUE DES FAUSSES SIMULATION UNTIL NOW
        reference_data=rawdata
        # On récupère la liste des paramètres à inférer (nom + nombre)
        list_param=inspect.signature(current_mod)
        to_opt=list(list_param.parameters.values())[1].default
        ### Definir la plage x, y et les paramètres à optimiser
        # Définition des valeurs de paramètres à priori
        prior=generate_prior(to_opt)
        bounds = [(1e-6, 2000),(1e-6, 10),(0.1, 5)]
        # Exctraction des données nécessaires
        # y_obs=reference_data["PAR"]
        # x_obs=reference_data["ETR"]
        ### Exécuter l'optimisation et récupérer la distance
        res=minimize(current_dist,x0=prior,args=(current_mod,rawdata,dist_to_merge,ponderation),bounds=bounds[0:len(to_opt)])
        ### Récupérer les valeurs de paramètres optimisé.
        final={}
        for i in range(len(to_opt)):
            final[to_opt[i]]=res.x[i]
        optim={}
        optim["optimized_parameters"]=final
        optim["minimal_dist"]=res.fun
        return optim
    else:
        raise TypeError("Either distances or models are not list of str or str")


def flatten_dist(dic,path=None):
    #######################
    # Cette fonction applatti les sorties de optimize (arbre) en un dictionnaire structuré comme tel:
    # {'distname,modelname':{'param':{'alpha':value,..},'dist':value}}
    #######################
    flatten={}
    if path==None:
        path=[]
    if isinstance(dic,dict):
        for key, values in dic.items():
            if key!="optimized_parameters" and key!="minimal_dist":
                new_path=path+[key]
                sub_flatten=flatten_dist(values,new_path)
                flatten.update(sub_flatten)

            elif key=="minimal_dist":
                flatten[",".join(path)]=dic["minimal_dist"]
    return(flatten)

def get_best_prediction(dic):
    #####################
    # Cette fonction renvoie le modèle dont l'optimisation a renvoyé la plus petite distance
    # Elle prend en entrée la sortie de la fonction optimize
    ####################
    dic=flatten_dist(dic)
    best_prediction_per_distance={}
    for key,value in dic.items():
        if key.split(",")[1] not in best_prediction_per_distance:
            best_prediction_per_distance[key.split(",")[1]]=[key.split(",")[0],value]
        elif value<best_prediction_per_distance[key.split(",")[1]][1]:
            best_prediction_per_distance[key.split(",")[1]]=[key.split(",")[0],value]
        else: 
            pass

    return best_prediction_per_distance
        

def generate_prior(parameter_name):
    #####################
    # Cette fonction à pour objectif de fixer les valeurs initiales des paramètres à l'initialisation
    # Attention de bien modifier le prior_dic en cas d'ajout d'un modèle contenant des paramètres n'étant pas déjà dans ce dernier
    ####################
    prior_dic={"ETR":40,"alpha":0.2,"m":1}
    try:
        prior_list=[prior_dic[param] for param in parameter_name]
    except:
        raise ValueError("Prior(s) de paramètres non défini(s)")
    return prior_list

def Simulate(data,models,distances,merge_dist=False,merge_only=False,ponderation=[0.5,0.5]):
    ######################
    # Cette fonction est utilisée comme finalité à toutes les fonctions de ce fichier.
    # Elle prend en entrée les données sous forme de data frame pandas, les modeles sous forme de liste de str,
    # les distances sous forme de liste de distance, la validité de la distance fusionnée, l'unicité de la distance fusionnée
    # et la pondération entre les distances fusionnées
    ######################
    raw_data=data
    # On ajoute ou remplace aux distances la distance fusionnée 
    if merge_dist and not(merge_only):
        distances.append("merge."+".".join(distances))
    if merge_only:
        distances=["merge."+".".join(distances)]
    # rawdata=data_loading.load(path)
    # Réalisation de l'optimisation
    optimized_parameters=optimize_models(models,distances,data,ponderation)
    # On récupère la meilleure optimisation pour chaque distance
    best_optimization_per_distance=get_best_prediction(optimized_parameters)
    # On récupère le meilleur modèle pour chaque distance
    average_best_model=[value[0] for key,value in best_optimization_per_distance.items()]
    # On récupère les paramètres pour chaque distance
    best_opt_param={",".join([key,value[0]]): optimized_parameters[value[0]][key]["optimized_parameters"] for key,value in best_optimization_per_distance.items()}
    # On renvoie les meilleurs optimisations et les meilleurs paramètres
    return best_opt_param,best_optimization_per_distance
# a=optimize_models(["Model1","Model2","Model3","Model4"],["least_square_distance","least_square_distance2","merge.least_square_distance.least_square_distance2"],models.Model6([0,1,2,3],[0.5,0.5]),[0.5,0.5])
# print(a)
# print(get_best_prediction(a))

