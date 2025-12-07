import models
import data_loading
import numpy
import inspect
def extract_models_parameters(modname):
    if isinstance(modname,list):
        multi_mod_param={}
        for single_model in modname:
            multi_mod_param[single_model]=extract_models_parameters(single_model)
        return(multi_mod_param)
    if isinstance(modname,str):
        mod_param={}
        try:
            current_mod = getattr(models, modname)
            list_param=inspect.signature(current_mod)
            for param_name, param in list_param.parameters.items():
                if param_name=="E":
                    mod_param["E"]="fixed"
                if param_name=="alpha":
                    mod_param["alpha"]="to_opt"
                if param_name=="ETRmax":
                    mod_param["ETRmax"]="to_opt"
            return(mod_param)
        except:
            raise ValueError("model name not defined")
    if not(isinstance(modname,str)) and not(isinstance(modname,list)):
        raise TypeError("please enter either a str or list of str as model to extract parameters from")

def optimize_models(modname,dist):
    if isinstance(modname,list):
        multi_mod_param_opti={}
        for single_model in modname:
            multi_mod_param_opti[single_model]=optimize_models(single_model)
        return(multi_mod_param)
    if isinstance(modname,str):
        reference_data=data_loading(None)
        to_opt_or_not_to_opt=extract_models_parameters(modname)
        current_dist=getattr(distance,dist)
        ### Definir la plage x, y et les paramètres à optimiser
        ### Exécuter l'optimisation et récupérer la distance?
        ### Récupérer les valeurs de paramètres optimisé.




