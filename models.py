##### The goal of this file is to define as many models as wanted to use for optimization
### Modele structure type :
## 1. Definition du modèle
# Le modèle doit prendre en entrée une liste de valeur d'un paramètre connu (par exemple l'intensité lumineuse ou le temps)
# Et une liste de paramètre à estimer (numérique). Il est nécessaire que le nom des paramètres soit défini sous
# frome de liste de chaine de caractère dans les valeurs par défault puisque ces valeurs par défaut sont utilisées
# afin de rendre optimizer généralisant.
## 2. Déclaration des paramètres : les paramètres doivent être extrait de la liste de paramètre à estimer
## 3. S'assurer que le vecteur de paramètre soit bien un objet numpy
## 4. Calcule et renvoie de la distance
import numpy as np 
def Model1(E,param=["alpha","ETR"]):
    alpha=param[0]
    ETR=param[1]
    E = np.atleast_1d(E)
    return((ETR*alpha*E)/((ETR*alpha)+E))
def Model2(E,param=["alpha","ETR"]):
    alpha=param[0]
    ETR=param[1]
    E = np.atleast_1d(E)
    return(ETR*(1-np.exp(-(alpha*E)/ETR)))
def Model3(E,param=["alpha","ETR"]):
    alpha=param[0]
    ETR=param[1]
    E = np.atleast_1d(E)
    return(ETR*np.tanh((alpha*E)/ETR))
def Model4(E,param=["alpha","ETR","m"]):
    alpha=param[0]
    ETR=param[1]
    m=param[2]
    E = np.atleast_1d(E)
    return((ETR*E)/((ETR/alpha)**m+E**m)**(1/m))
# def Model5(E,alpha,ETR):
#     return()
def Model6(E,param=["alpha","ETR"]):
    alpha=param[0]
    ETR=param[1]
    E = np.atleast_1d(E)
    return(alpha*E*np.exp(-((alpha*E)/(ETR*np.exp(1)))))

def Model7(E,param=["alpha","ETR_pot", "B"]) :
    alpha=param[0]
    ETR_pot=param[2]
    B=param[3]
    E = np.atleast_1d(E)
    return(ETR_pot*(1-exp((alpha*E/ETR_pot)))*exp((B*E)/ETR_pot)

def Model8(E,param=["alpha","ETR", "E_opt"]) :
    alpha=param[0]
    ETR=param[2]
    E_opt=param[3]
    E = np.atleast_1d(E)
    return(E/((1/(alpha*E_opt*E_opt))*E*E+((1/ETR)-(2/(alpha*E_opt))*E+1/alpha)

def Model9(E,param=["alpha","K1", "E_opt"]) :
    alpha=param[0]
    K1=param[2]
    E_opt=param[3]
    E = np.atleast_1d(E)
    return((E_opt*E*exp(E/K1))/((E_opt/alpha)+E))

def Model10(E,param=["alpha","Ib", "E_opt"]) :
    alpha=param[0]
    Ib=param[2]
    E_opt=param[3]
    E = np.atleast_1d(E)
    return(alpha*(((1-E/Ib)*E)/(1+(alpha/E_opt)*E)))


# def Model7(E,alpha,ETR):
#     return()
# #def Model8(E,alpha,ETR):
# #    return()
# #def Model9(E,alpha,ETR):
#     return()
# #def Model10(E,alpha,ETR):
#     return()
