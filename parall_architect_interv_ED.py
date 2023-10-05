# -*- coding: utf-8 -*-
"""    
    Architectural interventions to mitigate the spread of
    SARS-CoV-2 in emergency departments
    
    InnoBRI project 
    This work was supported by the Innovation Funds of the 
    Joint Federal Committee 
    (Innovationsfonds des gemeinsamen Bundesausschusses (G-BA),
     funding reference: 01VSF19032)
    
    NOTE: FILE FOR Launching parallel tasks (scenarios)
    
@author: Gustavo Hernandez Mejia

"""

from funct_architect_interv_ED import *
from main_architect_interv_ED import *
import scipy.stats
import seaborn as sns
import collections, numpy
import concurrent.futures


t1 = time.perf_counter()

#------      Number of runs
runs = 1000
save_PAT = []
save_HCW = []

if __name__ == '__main__': 
    save_results = []
    save_results1 = []
    with concurrent.futures.ProcessPoolExecutor() as executor: 
        future_results =  [executor.submit(main_funct) for _ in range(runs)]
        for fut in concurrent.futures.as_completed(future_results):
            # print(fut.result())
            print(fut.done())
            save_results.append(fut.result()) 
            counter = 0
          
        Recep_P = []
        Triag_P = []
        WaitU_P = []
        WaitN_P = []
        AtteU_P = []
        AtteN_P = []
        Imagi_P = []
        Labot_P = []
        
        Recep_prop_H = []
        Triag_prop_H = []
        AtteU_prop_H = []
        AtteN_prop_H = []
        Imagi_prop_H = []
        Labot_prop_H = []
        Base1_prop_H = []
        Base2_prop_H = []
        Base3_prop_H = []
        
        Total_infect = []
        Total_infe_P = []
        Total_infe_H = []
        
        Recep_num_P_P = []
        Recep_num_P_H = []
        Recep_num_H_P = []
        Recep_num_H_H = []
        
        Triag_num_P_P = []
        Triag_num_P_H = []
        Triag_num_H_P = []
        Triag_num_H_H = []
        
        WaitU_P_P = []
        WaitN_P_P = []
        
        AtteU_num_P_P = []
        AtteU_num_P_H = []
        AtteU_num_H_P = []
        AtteU_num_H_H = []
        
        AtteN_num_P_P = []
        AtteN_num_P_H = []
        AtteN_num_H_P = []
        AtteN_num_H_H = []
        
        Imagi_num_P_P = []
        Imagi_num_P_H = []
        Imagi_num_H_P = []
        Imagi_num_H_H = []
        
        Labot_num_P_P = []
        Labot_num_P_H = []
        Labot_num_H_P = []
        Labot_num_H_H = []
        
        Base1_num_H = []
        Base2_num_H = []
        Base3_num_H = []

        for i in range(len(save_results)):
            Recep_P.append(save_results[i][0][0][0])
            Triag_P.append(save_results[i][0][0][1])
            WaitU_P.append(save_results[i][0][0][2])
            WaitN_P.append(save_results[i][0][0][3])
            AtteU_P.append(save_results[i][0][0][4])
            AtteN_P.append(save_results[i][0][0][5])
            Imagi_P.append(save_results[i][0][0][6])
            Labot_P.append(save_results[i][0][0][7])
            
            Recep_prop_H.append(save_results[i][0][1][0])
            Triag_prop_H.append(save_results[i][0][1][1])
            AtteU_prop_H.append(save_results[i][0][1][2])
            AtteN_prop_H.append(save_results[i][0][1][3])
            Imagi_prop_H.append(save_results[i][0][1][4])
            Labot_prop_H.append(save_results[i][0][1][5])
            Base1_prop_H.append(save_results[i][0][1][6])
            Base2_prop_H.append(save_results[i][0][1][7])
            Base3_prop_H.append(save_results[i][0][1][8])

        
        for i in range(len(save_results)):
            Recep_num_P_P.append(Recep_P[i][2])
            Recep_num_P_H.append(Recep_P[i][3])
            Recep_num_H_P.append(Recep_prop_H[i][2])
            Recep_num_H_H.append(Recep_prop_H[i][3])
            
            Triag_num_P_P.append(Triag_P[i][2])
            Triag_num_P_H.append(Triag_P[i][3])
            Triag_num_H_P.append(Triag_prop_H[i][2])
            Triag_num_H_H.append(Triag_prop_H[i][3])
            
            WaitU_P_P.append(WaitU_P[i][2])
            WaitN_P_P.append(WaitN_P[i][2])
            
            AtteU_num_P_P.append(AtteU_P[i][2])
            AtteU_num_P_H.append(AtteU_P[i][3])
            AtteU_num_H_P.append(AtteU_prop_H[i][2])
            AtteU_num_H_H.append(AtteU_prop_H[i][3])
            
            AtteN_num_P_P.append(AtteN_P[i][2])
            AtteN_num_P_H.append(AtteN_P[i][3])
            AtteN_num_H_P.append(AtteN_prop_H[i][2])
            AtteN_num_H_H.append(AtteN_prop_H[i][3])
            
            Imagi_num_P_P.append(Imagi_P[i][2])
            Imagi_num_P_H.append(Imagi_P[i][3])
            Imagi_num_H_P.append(Imagi_prop_H[i][2])
            Imagi_num_H_H.append(Imagi_prop_H[i][3])
            
            Labot_num_P_P.append(Labot_P[i][2])
            Labot_num_P_H.append(Labot_P[i][3])
            Labot_num_H_P.append(Labot_prop_H[i][2])
            Labot_num_H_H.append(Labot_prop_H[i][3])
            
            Base1_num_H.append(Base1_prop_H[i][3])
            Base2_num_H.append(Base2_prop_H[i][3])
            Base3_num_H.append(Base3_prop_H[i][3])
        
        
        Tot_Recep_P = [x + y for x, y in zip(Recep_num_P_P, Recep_num_P_H)]
        Tot_Recep_H = [x + y for x, y in zip(Recep_num_H_P, Recep_num_H_H)]
        Tot_Recep = [x + y for x, y in zip(Tot_Recep_P, Tot_Recep_H)]
        
        Tot_Triag_P = [x + y for x, y in zip(Triag_num_P_P, Triag_num_P_H)]
        Tot_Triag_H = [x + y for x, y in zip(Triag_num_H_P, Triag_num_H_H)]
        Tot_Triag = [x + y for x, y in zip(Tot_Triag_P, Tot_Triag_H)]
        
        Tot_WaitU = WaitU_P_P
        Tot_WaitN = WaitN_P_P
        
        Tot_AtteU_P = [x + y for x, y in zip(AtteU_num_P_P, AtteU_num_P_H)]
        Tot_AtteU_H = [x + y for x, y in zip(AtteU_num_H_P, AtteU_num_H_H)]
        Tot_AtteU  = [x + y for x, y in zip(Tot_AtteU_P, Tot_AtteU_H)]
        
        Tot_AtteN_P = [x + y for x, y in zip(AtteN_num_P_P, AtteN_num_P_H)]
        Tot_AtteN_H = [x + y for x, y in zip(AtteN_num_H_P, AtteN_num_H_H)]
        Tot_AtteN  = [x + y for x, y in zip(Tot_AtteN_P, Tot_AtteN_H)]
        
        Tot_Imagi_P = [x + y for x, y in zip(Imagi_num_P_P, Imagi_num_P_H)]
        Tot_Imagi_H = [x + y for x, y in zip(Imagi_num_H_P, Imagi_num_H_H)]
        Tot_Imagi  = [x + y for x, y in zip(Tot_Imagi_P, Tot_Imagi_H)]
        
        Tot_Labot_P = [x + y for x, y in zip(Labot_num_P_P, Labot_num_P_H)]
        Tot_Labot_H = [x + y for x, y in zip(Labot_num_H_P, Labot_num_H_H)]
        Tot_Labot  = [x + y for x, y in zip(Tot_Labot_P, Tot_Labot_H)]
        
        Tot_Base1 = Base1_num_H
        Tot_Base2 = Base2_num_H
        Tot_Base3 = Base3_num_H
        
        
        Total_infect = [(x + y + q + w + r + t + z + u + a + s + f) 
                     for x, y, q, w, r, t, z, u, a, s, f in zip(Tot_Recep, 
              Tot_Triag, Tot_WaitU, Tot_WaitN, Tot_AtteU, Tot_AtteN, Tot_Imagi,
                     Tot_Labot, Tot_Base1, Tot_Base2, Tot_Base3)]
        
        Total_infe_P = [(x + y + q + w + r + t + z + u) 
                     for x, y, q, w, r, t, z, u in zip(Tot_Recep_P, 
                  Tot_Triag_P, Tot_WaitU, Tot_WaitN, Tot_AtteU_P, Tot_AtteN_P, 
                                Tot_Imagi_P, Tot_Labot_P)]
        
        Total_infe_H = [(x + y + q + w + r + t + z + u + f) 
                     for x, y, q, w, r, t, z, u, f in zip(Tot_Recep_H, 
                  Tot_Triag_H, Tot_AtteU_H, Tot_AtteN_H, Tot_Imagi_H, 
                  Tot_Labot_H, Tot_Base1, Tot_Base2, Tot_Base3 )]
        

    palettes = iter(sns.husl_palette(7))

    
    """    
        Save Figure (general) Files
        Comment/uncomment for each scenario, 
        changing the saving path as required

    """
    mark_s = "6"
    cols = sns.color_palette("Set2",8)
    names = ['Total', 'Patients', 'HCW']
    f, ax3 = plt.subplots(figsize=(13,6), facecolor='w', edgecolor='k')
    # ax3.set_yscale("log")
    plt.rc('xtick', labelsize = 17) 
    plt.rc('ytick', labelsize = 17) 
    # sns.stripplot(data=[Base_TOT, F_co_TOT, Curt_TOT, Vent_TOT, V_Cu_TOT, 
    #                       N_VC_TOT, scre_TOT], color=".4")
    sns.boxplot(data=[Total_infect, Total_infe_P, Total_infe_H], 
                palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})   
    plt.xticks(np.arange(3), names) 
    # plt.ylim(top=400) 
    plt.title('Total of newly infected ', fontsize = 22)
    # plt.savefig('15_test_parall/totals_BCase.pdf', format='pdf', dpi=1400)
    

    Save_Total_inf = {'Recep': Tot_Recep, 'Triag': Tot_Triag, 
                      'WaitU': Tot_WaitU,
                      'WaitN': Tot_WaitN, 'AtteU': Tot_AtteU, 
                      'AtteN': Tot_AtteN,
                      'Imagi': Tot_Imagi, 'Labot': Tot_Labot, 
                      'Base1': Tot_Base1,
                      'Base2': Tot_Base2, 'Base3': Tot_Base3, 
                      'Total_inf': Total_infect}
    
    Save_Total_P = {'Recep_P': Tot_Recep_P, 'Triag_P': Tot_Triag_P, 
                    'WaitU_P': Tot_WaitU,   'WaitN_P': Tot_WaitN, 
                    'AtteU_P': Tot_AtteU_P, 
                    'AtteN_P': Tot_AtteN_P, 'Imagi_P': Tot_Imagi_P,
                    'Labot_P': Tot_Labot_P,
                    'Total_inf_P': Total_infe_P}
    
    Save_Total_H = {'Recep_H': Tot_Recep_H, 'Triag_H': Tot_Triag_H, 
                    'AtteU_H': Tot_AtteU_H, 
                    'AtteN_H': Tot_AtteN_H, 'Imagi_H': Tot_Imagi_H, 
                    'Labot_H': Tot_Labot_H, 'Base1': Tot_Base1, 
                      'Base2': Tot_Base2,   'Base3': Tot_Base3,
                'Total_inf_H': Total_infe_H}
    
    Save_from_whom = {
            'Recep_num_P_P': Recep_num_P_P,'Recep_num_P_H': Recep_num_P_H,
            'Recep_num_H_P': Recep_num_H_P,'Recep_num_H_H': Recep_num_H_H,
    
            'Triag_num_P_P': Triag_num_P_P,'Triag_num_P_H': Triag_num_P_H,
            'Triag_num_H_P': Triag_num_H_P,'Triag_num_H_H': Triag_num_H_H,
            
            'WaitU_P_P': WaitU_P_P,'WaitN_P_P': WaitN_P_P,
            
            'AtteU_num_P_P': AtteU_num_P_P,'AtteU_num_P_H': AtteU_num_P_H,
            'AtteU_num_H_P': AtteU_num_H_P,'AtteU_num_H_H': AtteU_num_H_H,
            
            'AtteN_num_P_P': AtteN_num_P_P,'AtteN_num_P_H': AtteN_num_P_H,
            'AtteN_num_H_P': AtteN_num_H_P,'AtteN_num_H_H': AtteN_num_H_H,
            
            'Imagi_num_P_P': Imagi_num_P_P,'Imagi_num_P_H': Imagi_num_P_H,
            'Imagi_num_H_P': Imagi_num_H_P,'Imagi_num_H_H': Imagi_num_H_H,
            
            'Labot_num_P_P': Labot_num_P_P,'Labot_num_P_H': Labot_num_P_H,
            'Labot_num_H_P': Labot_num_H_P,'Labot_num_H_H': Labot_num_H_H,
            
            'Base1_num_H': Base1_num_H,'Base2_num_H': Base2_num_H,
            'Base3_num_H': Base3_num_H  }
    
    
    
    """    
        Save Data Files
        Comment/uncomment for each scenario
        Change the saving path as required

    """
    # Save_Total_infect = pd.DataFrame(data=Save_Total_inf)
    # Save_Total_infect.to_excel("15_test_parall\Base_Total.xlsx")
    
    # Save_Total_Pat = pd.DataFrame(data=Save_Total_P)
    # Save_Total_Pat.to_excel("15_test_parall\Base_Total_Pat.xlsx")
    
    # Save_Total_HCW = pd.DataFrame(data=Save_Total_H)
    # Save_Total_HCW.to_excel("15_test_parall\Base_Total_HCW.xlsx")

    # Save_from = pd.DataFrame(data=Save_from_whom)
    
    # Save_from.to_excel("15_test_parall\Base_from_whom.xlsx")
    
    t2 = time.perf_counter()
            
    print("finished in " + str(round((t2-t1)/60,2))   + " minute(s)")         
            

