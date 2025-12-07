import numpy as np


def least_square_distance(param,model,x,y_ref):
    # current_mod=getattr(models,model)
    y_pred=model(x,param)
    dist=sum((y_ref-y_pred)**2)
    return dist


