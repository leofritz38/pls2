
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
def create_fig(Path,data_proportion,model_used,dist,figname):
    df=pd.read_csv(Path, sep=";", decimal=".")
    df.replace("-", np.nan, inplace=True)
    # df["ETR"] = pd.to_numeric(df["ETR"], errors="coerce")
    cols = df.columns  # ou tu peux choisir certaines colonnes : cols = ["ETR", "PAR"]
    df["PAR"] = pd.to_numeric(df["PAR"], errors='coerce')
    df["ETR"] = pd.to_numeric(df["ETR"], errors='coerce')
    df_clean = df.dropna(subset=["PAR","ETR"])
    # dist=["least_square_distance_ETR"]
    # model_used=["Model2"]
    alpha={i:[] for i in dist}
    ETRmax={i:[] for i in dist}
    predicted={i:[] for i in dist}
    # data_proportion=120001
    time_seq=range(10,data_proportion,10)
    percent=0.01
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
        if i/time_seq[len(time_seq)-1]>percent:
           print(percent,"% simulation done")
           percent+=0.01
    for key,value in alpha.items():
        plt.title("alpha")
        plt.scatter(time_seq,value,s=5)
        plt.savefig(figname+"alpha"+key+".png")
        plt.show()

    for key,value in ETRmax.items():
        plt.title(path[1])
        plt.ylim(0, 100) 
        plt.scatter(time_seq,value,s=5)
        plt.savefig(figname+"ETRmax"+key+".png")
        plt.show()

    for key,value in predicted.items(): 
        print(len(value))  
        plt.title(key)
        plt.plot(range(data_proportion-1),value,color="red")
        plt.plot(range(data_proportion-1),df["rETR"][:data_proportion-1])
        plt.savefig(figname+"predicted_vs_fitted"+key+".png")
        plt.show()
    return ("Done")
PATH="C:/Users/Nitro/Downloads/data/data/Online PAM/00_process_data/00_rlc_data/00_10s/01_pam3/data_PAM_LR_070_G1_MI5_MEA10_10s_PAM3.csv"
dist=["least_square_distance_ETR"]
model_used=["Model2"]
figname="Pam3_10s "
data_proportion=120001
create_fig(PATH,data_proportion,model_used,dist,figname)

print("data need to be extracted fom file.zip in order ot be readen by read_csv")
print(" give the data_file pathway with / not \ ")

#file_name="data_algae/Online_PAM/00_process_data/00_rlc_data/00_5s/00_pam1/data_PAM_LR_070_batch_G1_MI5_MEA10_5s_PAM1.csv"

def file_downloader(file_name):
    data=pandas.read_csv(file_name, sep=";", decimal=".")
    # print(data.head(), "all the data files")
    data_interst=data.loc[:,["t in s","PAR","ETR","rETR","F","Fm'","Y(II)"]] 
    print(data_interst.head(),"only the data of interest")
    
    return (data_interst)


# file_nameT=argv[1]
# data_algea=file_downloader(file_name=file_nameT)


