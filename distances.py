import numpy as np
import pandas as pd


def least_square_distance_ETR(param,model,data):
    # current_mod=getattr(models,model)
    x = pd.to_numeric(data["PAR"], errors='coerce').to_numpy()
    y_ref = pd.to_numeric(data["rETR"], errors='coerce').to_numpy()
    y_pred=model(x,param)
    # masque pour ignorer les NaN dans y_ref ou y_pred
    mask = ~np.isnan(y_ref) & ~np.isnan(y_pred)

    # distance moyenne quadratique
    dist = np.sum((y_ref[mask] - y_pred[mask])**2) / mask.sum()
    return dist
def least_square_distance_median(param,model,data):
    # current_mod=getattr(models,model)
    x = pd.to_numeric(data["PAR"], errors='coerce').to_numpy()
    y_ref = pd.to_numeric(data["rETR"], errors='coerce').to_numpy()
    y_pred=model(x,param)
    mask = ~np.isnan(y_ref) & ~np.isnan(y_pred)

    # carré des différences
    squared_diff = (y_ref[mask] - y_pred[mask])**2

    # médiane
    dist = np.median(squared_diff)
    return dist
def merge_distance(param,model,data,dist_to_merge,ponderation):
    if len(ponderation)!=len(dist_to_merge):
        raise ValueError("Must be the same amount of distances to merge and ponderation")
    dist=0
    for i in range(0,len(dist_to_merge)):
        current_dist=globals()[dist_to_merge[i]]
        dist_value=ponderation[i]*current_dist(param,model,data)
        dist+=dist_value
    dist=dist
    return dist




