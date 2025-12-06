
import pandas
from sys import argv


print("data need to be extracted fom file.zip in order ot be readen by read_csv")
print(" give the data_file pathway with / not \ ")
file_name=argv[1]
#file_name="data_algae/Online_PAM/00_process_data/00_rlc_data/00_5s/00_pam1/data_PAM_LR_070_batch_G1_MI5_MEA10_5s_PAM1.csv"



data=pandas.read_csv(file_name, sep=";", decimal=".")
print(data.head(), "all the data files")
data_interst=data.loc[:,["PAR","ETR","rETR","F","Fm'","Y(II)"]]
print(data_interst.head(),"only the data of interest")