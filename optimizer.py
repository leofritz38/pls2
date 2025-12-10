import models
# import data_loading
from scipy.optimize import minimize
import numpy as np
import inspect
import types
import distances
### Deprecated
# def extract_models_parameters(modname):
#     if isinstance(modname,list):
#         multi_mod_param={}
#         for single_model in modname:
#             multi_mod_param[single_model]=extract_models_parameters(single_model)
#         return(multi_mod_param)
#     elif isinstance(modname,str):
#         mod_param={}
#         try:
#             current_mod = getattr(models, modname)
#             list_param=inspect.signature(current_mod)
#             for param_name, param in list_param.parameters.items():
#                 if param_name=="E":
#                     try:
#                         mod_param["fixed"].append(param_name)
#                     except:
#                         mod_param["fixed"]=[param_name]
#                 else:
#                     try:
#                         mod_param["to_opt"].append(param_name)
#                     except:
#                         mod_param["to_opt"]=[param_name]
#             if len(mod_param["fixed"])==0:
#                 raise ValueError("E must be a parameter of the model")
#             return(mod_param)
#         except:
#             raise ValueError("model name not defined")
#     else:
#         raise TypeError("please enter either a str, a list or a self_define model of str as model to extract parameters from")

def optimize_models(modname,dist,rawdata,ponderation):
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
        # y_obs=reference_data["PAR"]
        # x_obs=reference_data["ETR"]
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
    prior_dic={"ETR":40,"alpha":0.2,"m":1}
    prior_list=[prior_dic[param] for param in parameter_name]
    return prior_list          
# a=optimize_models(["Model1","Model2","Model3","Model4"],["least_square_distance","least_square_distance2","merge.least_square_distance.least_square_distance2"],models.Model6([0,1,2,3],[0.5,0.5]),[0.5,0.5])
# print(a)
# print(get_best_prediction(a))