
import pandas as pd
import numpy as np  
import decision_making
from sys import argv
import matplotlib.pyplot as plt
import models

# print("data need to be extracted fom file.zip in order ot be readen by read_csv")
# print(" give the data_file pathway with / not \ ")
# file_name=argv[1]
# #file_name="data_algae/Online_PAM/00_process_data/00_rlc_data/00_5s/00_pam1/data_PAM_LR_070_batch_G1_MI5_MEA10_5s_PAM1.csv"

# df=pd.read_csv("C:/Users/Nitro/Downloads/data/data/Online PAM/00_process_data/00_rlc_data/00_5s/00_pam1/data_PAM_LR_070_G1_MI5_MEA10_5s_PAM1.csv", sep=";", decimal=".")


# data=pandas.read_csv(file_name, sep=";", decimal=".")
# print(data.head(), "all the data files")
# data_interst=data.loc[:,["PAR","ETR","rETR","F","Fm'","Y(II)"]]
# print(data_interst.head(),"only the data of interest")


df=pd.read_csv("C:/Users/Nitro/Downloads/data/data/Online PAM/00_process_data/00_rlc_data/00_10s/01_pam3/data_PAM_LR_070_G1_MI5_MEA10_10s_PAM3.csv", sep=";", decimal=".")
df.replace("-", np.nan, inplace=True)
# df["ETR"] = pd.to_numeric(df["ETR"], errors="coerce")
cols = df.columns  # ou tu peux choisir certaines colonnes : cols = ["ETR", "PAR"]
df["PAR"] = pd.to_numeric(df["PAR"], errors='coerce')
df["ETR"] = pd.to_numeric(df["ETR"], errors='coerce')
df_clean = df.dropna(subset=["PAR","ETR"])
dist=["least_square_distance_ETR"]
model_used=["Model2"]
alpha={i:[] for i in dist}
ETRmax={i:[] for i in dist}
predicted={i:[] for i in dist}
data_proportion=120001
time_seq=range(10,data_proportion,10)
for i in time_seq:
    best_param,bestmodel=decision_making.decision_making(df.iloc[i-10:i],model_used,dist,merge_dist=False,merge_only=False,ponderation=[0.5,0.5])
    paths=[[key,value[0]] for key,value in bestmodel.items()]
    for path in paths:
        key=",".join(path)
        full_param=best_param[key]
        param=[value for key,value in full_param.items()]
        alpha[path[0]]+=[param[0]]
        ETRmax[path[0]]+=[param[1]]
        model=getattr(models,path[1])
        predicted[path[0]]+=list(model(df["PAR"][i-10:i],param))
    print(i)
for key,value in alpha.items():
    plt.title("alpha")
    print(len(value))
    plt.scatter(time_seq,value)
    plt.savefig("alpha"+key+".png")
    plt.show()

for key,value in ETRmax.items():
    plt.title(path[1])
    plt.scatter(time_seq,value)
    plt.savefig("ETRmax"+key+".png")
    plt.show()
print(len(range(data_proportion-1)))
print(len(df["rETR"][:data_proportion-1]))

for key,value in predicted.items(): 
    print(len(value))  
    plt.title(key)
    plt.plot(range(data_proportion-1),value,color="red")
    plt.plot(range(data_proportion-1),df["rETR"][:data_proportion-1])
    plt.savefig("predicted_vs_fitted"+key+".png")
    plt.show()
