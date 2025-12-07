##### The goal of this file is to define as many models as wanted to use for optimization
import numpy as np 
def Model1(E,param=["ETRmax","alpha"]):
    alpha=param[0]
    ETRmax=param[1]
    E = np.atleast_1d(E)
    return((ETRmax*alpha*E)/((ETRmax*alpha)+E))
def Model2(E,param=["ETRmax","alpha"]):
    alpha=param[0]
    ETRmax=param[1]
    E = np.atleast_1d(E)
    return(ETRmax*(1-np.exp(-(alpha*E)/ETRmax)))
def Model3(E,param=["ETRmax","alpha"]):
    alpha=param[0]
    ETRmax=param[1]
    E = np.atleast_1d(E)
    return(ETRmax*np.tanh((alpha*E)/ETRmax))
def Model4(E,param=["ETRmax","alpha","m"]):
    alpha=param[0]
    ETRmax=param[1]
    m=param[2]
    E = np.atleast_1d(E)
    return((ETRmax*E)/((ETRmax/alpha)**m+E**m)**(1/m))
# def Model5(E,alpha,ETRmax):
#     return()
def Model6(E,param=["ETRmax","alpha"]):
    alpha=param[0]
    ETRmax=param[1]
    E = np.atleast_1d(E)
    return(alpha*E*np.exp(-((alpha*E)/(ETRmax*np.exp(1)))))
# def Model7(E,alpha,ETRmax):
#     return()
# #def Model8(E,alpha,ETRmax):
# #    return()
# #def Model9(E,alpha,ETRmax):
#     return()
# #def Model10(E,alpha,ETRmax):
#     return()
