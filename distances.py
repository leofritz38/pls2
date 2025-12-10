import numpy as np


def least_square_distance_ETR(param,model,data):
    # current_mod=getattr(models,model)
    x=data["PAR"]
    y_ref=data["ETR"]
    y_pred=model(x,param)
    dist=(1/len(y_pred))*sum((y_ref-y_pred)**2)
    return dist
def least_square_distance_median(param,model,data):
    # current_mod=getattr(models,model)
    x=data["PAR"]
    y_ref=data["ETR"]
    y_pred=model(x,param)
    dist= np.median((y_ref - y_pred)**2)
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




