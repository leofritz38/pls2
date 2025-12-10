import numpy as np


def least_square_distance(param,model,x,y_ref):
    # current_mod=getattr(models,model)
    y_pred=model(x,param)
    dist=sum((y_ref-y_pred)**2)
    return dist
def least_square_distance2(param,model,x,y_ref):
    # current_mod=getattr(models,model)
    y_pred=model(x,param)
    dist=sum((y_ref-y_pred)**2)
    return dist
def merge_distance(param,model,x,y_ref,dist_to_merge,ponderation):
    if len(ponderation)!=len(dist_to_merge):
        raise ValueError("Must be the same amount of distances to merge and ponderation")
    dist=0
    for i in range(0,len(dist_to_merge)):
        current_dist=globals()[dist_to_merge[i]]
        dist_value=ponderation[i]*current_dist(param,model,x,y_ref)
        dist+=dist_value
    dist=dist
    return dist




