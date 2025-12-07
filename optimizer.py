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

def optimize_models(modname,dist,pseudo_ref):
    # Premier cas de figure, plusieurs modèles qui tournent
    if isinstance(modname,list):
        # On execute la fonction sur chaque modèle individuel puis on stock le tout dans un dico de la strcture suivante :
        # {mod_name:{dist_name:{parametre_opti:list,min_dist:value}}}
        # Si une seule distance alors le dictionnaire ne contient pas de section dist_name
        multi_mod_param_opti={}
        for single_model in modname:
            multi_mod_param_opti[single_model]=optimize_models(single_model,dist,pseudo_ref)
        return(multi_mod_param_opti)
    elif isinstance(dist,list):
        # On execute la fonction sur chaque modèle individuellement
        multi_dist_param_opti={}
        for single_dist in dist:
            multi_dist_param_opti[single_dist]=optimize_models(modname,single_dist,pseudo_ref)
        return(multi_dist_param_opti)
    elif isinstance(modname,str) and isinstance(dist,str):
        # On récupère la fonction de distance associé à la chaine de caractère
        current_dist=getattr(distances,dist)
        # On récupère le modèle associé à la chaine de caractère
        current_mod = getattr(models, modname)
        # On charge les datas
        reference_data=pseudo_ref
        # On récupère la liste des paramètres à inférer (nom + nombre)
        list_param=inspect.signature(current_mod)
        to_opt=list(list_param.parameters.values())[1].default
        ### Definir la plage x, y et les paramètres à optimiser
        # Définition des valeurs de paramètres à priori
        prior=np.repeat(0.5, len(to_opt))
        # Exctraction des données nécessaires
        # y_obs=reference_data["PAR"]
        # x_obs=reference_data["ETR"]
        y_obs=pseudo_ref
        x_obs=[0,1,2,3]
        ### Exécuter l'optimisation et récupérer la distance
        res=minimize(current_dist,x0=prior,args=(current_mod,x_obs,y_obs))
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
                flatten["_".join(path)]=dic["minimal_dist"]
    return(flatten)

def get_best_prediction(dic):
    paths=[key for key,value in dic.items()]
    distances=[value for key,value in dic.items()]
    best_prediction=paths[np.argmin(distances)]
    return best_prediction
        
                

