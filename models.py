##### The goal of this file is to define as many models as wanted to use for optimization
import math
def Model1(E,alpha,ETRmax):
    return((ETRmax*alpha*E)/((ETRmax*alpha)+E))
def Model2(E,alpha,ETRmax):
    return(ETRmax*(1-math.exp(-(alpha*E)/ETRmax)))
def Model3(E,alpha,ETRmax):
    return(ETRmax*math.tanh((alpha*E)/ETRmax))
def Model4(E,alpha,ETRmax):
    return()
def Model5(E,alpha,ETRmax):
    return()
def Model6(E,alpha,ETRmax):
    return()
def Model7(E,alpha,ETRmax):
    return()
def Model8(E,alpha,ETRmax):
    return()
def Model9(E,alpha,ETRmax):
    return()
def Model10(E,alpha,ETRmax):
    return()
