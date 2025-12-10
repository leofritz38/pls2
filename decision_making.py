### Goal of this file is to diagnostic according to parameter value
import optimizer
import distances
import models
import numpy

def decision_making(raw_data,models,distances,merge_dist=False,merge_only=False,ponderation):
    if merge_dist and not(merge_only):
        distances.append(".".join(distances))
    if merge_only:
        distances=[".".join(distances)]
    optimized_parameters=optimizer.optimize_models(models,distances,raw_data,ponderation)
    best_optimization_per_distance=optimizer.get_best_prediction(optimized_parameters)
    average_best_model=[value[0] for key,value in best_optimization_per_distance.items()]
    if np.all(average_best_model == average_best_model[0]):
        #Extraire les paramètres et conclure en précisant bien que toutes les distances convergent vers le même modèle
        #Choisir la dist la plus petite pour le modèle
        #recréer le chemin (modele, puis dist) pour récupérer les paramètres
        # Interpréter mécaniquement les paramètres et réponse --> table de décision plutôt que if elif pitié

    else:
        best_model = max(set(average_best_model), key=average_best_model.count)
        # Extraire et conclure sur ce dit modèle
        #Choisir la dist la plus petite pour le modèle majoritaire
        #recréer le chemin (modele, puis dist) pour récupérer les paramètres
        # Interpréter mécaniquement les paramètres et réponse --> table de décision plutôt que if elif pitié

