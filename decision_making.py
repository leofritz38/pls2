### L'objectif de ce fichier est de pouvoir prendre des décision au vu des imputs de PAM.
### En l'absence de données la prise de décision est factice
import optimizer
import distances
import models
import numpy as np
import pandas as pd
import time



def decision_making(tmax,df,model_used,dist,merge_dist=False,merge_only=False,ponderation=[0.5,0.5],proba_scenario=[0.3,0.3,0.4]):
    state=0
    time_since_recover=0
    time_since_stress=0
    t=10
    choice_scenario=np.random.multinomial(1,proba_scenario)
    scenario=build_scenario(choice_scenario,df,tmax)
    while t<tmax and state!=2:
        t=t+10
        best_param,bestmodel=optimizer.Simulate(scenario[t-10:t],model_used,dist,merge_dist=merge_dist,merge_only=merge_only,ponderation=ponderation)
        paths=[[key,value[0]] for key,value in bestmodel.items()]
        # On parcours les différentes distances (toujours un modèle par distance)
        alpha=[]
        ETRmax=[]
        for path in paths:
            # On récupère les valeurs de paramètres et on simule des données sur la plage de mesure
            key=",".join(path)
            full_param=best_param[key]
            param=[value for key,value in full_param.items()]
            alpha+=[param[0]]
            ETRmax+=[param[1]]
        alpha=np.mean(alpha)
        ETRmax=np.mean(ETRmax)
        # Si les valeurs de paramètres sont conjointement basses il existe éventuellement un stress
        if alpha<0.4 and ETRmax<150:
            # On laisse le bénéfice du doute à une erreur de mesure jusqu'à 10 pas de temps de stresse
            time_since_stress+=1
            if time_since_stress<10: 
                print("Time"+str(t)+"---> warning maybe pH stress")
            elif time_since_stress==10: 
                # Initialisation du stresse temporaire et envoie de CO2
                state=1
                print("Time"+str(t)+"--->Decision : Stress PH --> regularizing the pH")
            elif 50>time_since_stress>10:
                # Attente de la réponse des algues
                print("Time"+str(t)+"---> Decision : Stress PH --> waiting for regularizing of the pH")
            elif time_since_stress>50:
                # Si pas d'amélioration algues mortes et stresse acide
                state=2
                print("Time"+str(t)+"--->Decision: Acid pH stress happened, stopping the PAM")
        elif (alpha>0.4 or ETRmax>150) and state!=0:
            # Bénéfice du doute pour une erreur de mesure
            time_since_recover+=1
            if time_since_recover>10:
                # Récupération de l'état de santé des algues!!
                state=0
                maybe_state=0
                time_since_recover=0
                print("Time"+str(t)+"--->Stress recovered")
        elif (alpha>0.4 or ETRmax>150) and state==0:
            print("Time"+str(t)+"--->Everything okay")
        time.sleep(0.05)
    return choice_scenario

def build_scenario(choice_scenario,df,tmax):
    # Création d'une fake data_frame à partir de lignes connus pour être sans et avec stress pH en fonction des scenarios
    if choice_scenario[0]:
        ref_df=df[0:10]
        scenario=pd.concat([ref_df] * 200, ignore_index=True)
    elif choice_scenario[1]:
        ref_df=df[0:10]
        ref_df_stress=df[92940:92950]
        scenario = pd.concat(
            [ref_df] * 100
            + [ref_df_stress] * 49
            + [ref_df] * 51,
            ignore_index=True)

    elif choice_scenario[2]:
        ref_df=df[0:10]
        ref_df_stress=df[92940:92950]
        scenario = pd.concat(
            [ref_df] * 100
            + [ref_df_stress] * 100,
            ignore_index=True)
    return scenario

if __name__=='__main__':
    PATH="C:/Users/Nitro/Downloads/data/data/Online PAM/00_process_data/00_rlc_data/00_10s/01_pam3/data_PAM_LR_070_G1_MI5_MEA10_10s_PAM3.csv"
    df=pd.read_csv(PATH, sep=";", decimal=".")
    # Ici on peut changer les valeurs de probabilité des scénario -->[proba_0_stress,stress_basique,stress_acide]
    proba_scenario=[0,1,0]
    print(decision_making(2000,df,["Model2"],["least_square_distance_ETR"],merge_dist=False,merge_only=False,ponderation=[0.5,0.5],proba_scenario=proba_scenario))
