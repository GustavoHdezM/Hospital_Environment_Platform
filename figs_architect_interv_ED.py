# -*- coding: utf-8 -*-
"""    
    Architectural interventions to mitigate the spread of
    SARS-CoV-2 in emergency departments
    
    InnoBRI project 
    This work was supported by the Innovation Funds of the 
    Joint Federal Committee 
    (Innovationsfonds des gemeinsamen Bundesausschusses (G-BA),
     funding reference: 01VSF19032)
    
    NOTES: FILE FOR creating Figures
           Color format was adapted using Inkscape(.SVG) for manuscript
    
    
@author: Gustavo Hernandez Mejia

"""

# import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

"""                     
# ---------------------------      INTERVENTIONS     --------------------------

         1 - Base Case      
         2. Flexible Partitions (FP) 
         (in the code, the intervention can be found as "curtains")
         3. Attention Area Separation (AS)
         4. Holding Area Separation (HS)
         (in the code, the intervention can be found as "waiting separation")
         5. ED Base Separation (EBS)
         (in the code, ED Base can be found as "Nurse base")
         6. ED Base Extension (EBE)
         7. Ventilation (Vent)
         8. HS + AS
         9. FP + Vent
         10. AS + Vent
         11. EBE + Vent
         12. AS + EBE + Vent
# ---------------------------      INTERVENTIONS     --------------------------
"""  

Base_case_TOT = pd.read_excel('1_Base_case\Base_Total.xlsx', index_col=0)
Base_case_Pat = pd.read_excel('1_Base_case\Base_Total_Pat.xlsx', index_col=0)
Base_case_HCW = pd.read_excel('1_Base_case\Base_Total_HCW.xlsx', index_col=0)
Base_case_WHO = pd.read_excel('1_Base_case\Base_from_whom.xlsx', index_col=0)

Curtains_TOT = pd.read_excel('2_Flexi_Part\Base_Total.xlsx', index_col=0)
Curtains_Pat = pd.read_excel('2_Flexi_Part\Base_Total_Pat.xlsx', index_col=0)
Curtains_HCW = pd.read_excel('2_Flexi_Part\Base_Total_HCW.xlsx', index_col=0)
Curtains_WHO = pd.read_excel('2_Flexi_Part\Base_from_whom.xlsx', index_col=0)

FFP_TOT = pd.read_excel('3_Atten_Sep_AS\Base_Total.xlsx', index_col=0)
FFP_Pat = pd.read_excel('3_Atten_Sep_AS\Base_Total_Pat.xlsx', index_col=0)
FFP_HCW = pd.read_excel('3_Atten_Sep_AS\Base_Total_HCW.xlsx', index_col=0)
FFP_WHO = pd.read_excel('3_Atten_Sep_AS\Base_from_whom.xlsx', index_col=0)

NB_max_TOT = pd.read_excel('4_Hold_Sep_HS\Base_Total.xlsx', index_col=0)
NB_max_Pat = pd.read_excel('4_Hold_Sep_HS\Base_Total_Pat.xlsx', index_col=0)
NB_max_HCW = pd.read_excel('4_Hold_Sep_HS\Base_Total_HCW.xlsx', index_col=0)
NB_max_WHO = pd.read_excel('4_Hold_Sep_HS\Base_from_whom.xlsx', index_col=0)

NB_sppit_TOT = pd.read_excel('5_EDBase_Sep_EBS\Base_Total.xlsx', index_col=0)
NB_sppit_Pat = pd.read_excel('5_EDBase_Sep_EBS\Base_Total_Pat.xlsx', 
                             index_col=0)
NB_sppit_HCW = pd.read_excel('5_EDBase_Sep_EBS\Base_Total_HCW.xlsx', 
                             index_col=0)
NB_sppit_WHO = pd.read_excel('5_EDBase_Sep_EBS\Base_from_whom.xlsx', 
                             index_col=0)

NB_volm_TOT = pd.read_excel('6_EDBase_Ext_EBE\Base_Total.xlsx', index_col=0)
NB_volm_Pat = pd.read_excel('6_EDBase_Ext_EBE\Base_Total_Pat.xlsx', 
                            index_col=0)
NB_volm_HCW = pd.read_excel('6_EDBase_Ext_EBE\Base_Total_HCW.xlsx', 
                            index_col=0)
NB_volm_WHO = pd.read_excel('6_EDBase_Ext_EBE\Base_from_whom.xlsx',
                            index_col=0)

Ventilat_TOT = pd.read_excel('7_Ventilation\Base_Total.xlsx', index_col=0)
Ventilat_Pat = pd.read_excel('7_Ventilation\Base_Total_Pat.xlsx', index_col=0)
Ventilat_HCW = pd.read_excel('7_Ventilation\Base_Total_HCW.xlsx', index_col=0)
Ventilat_WHO = pd.read_excel('7_Ventilation\Base_from_whom.xlsx', index_col=0)

screenin_TOT = pd.read_excel('8_HS_AS\Base_Total.xlsx', index_col=0)
screenin_Pat = pd.read_excel('8_HS_AS\Base_Total_Pat.xlsx', index_col=0)
screenin_HCW = pd.read_excel('8_HS_AS\Base_Total_HCW.xlsx', index_col=0)
screenin_WHO = pd.read_excel('8_HS_AS\Base_from_whom.xlsx', index_col=0)

Vet_Curt_TOT = pd.read_excel('9_FP_Vent\Base_Total.xlsx', index_col=0)
Vet_Curt_Pat = pd.read_excel('9_FP_Vent\Base_Total_Pat.xlsx', index_col=0)
Vet_Curt_HCW = pd.read_excel('9_FP_Vent\Base_Total_HCW.xlsx', index_col=0)
Vet_Curt_WHO = pd.read_excel('9_FP_Vent\Base_from_whom.xlsx', index_col=0)

AS_Vent_TOT = pd.read_excel('10_AS_Vent\Base_Total.xlsx', index_col=0)
AS_Vent_Pat = pd.read_excel('10_AS_Vent\Base_Total_Pat.xlsx', index_col=0)
AS_Vent_HCW = pd.read_excel('10_AS_Vent\Base_Total_HCW.xlsx', index_col=0)
AS_Vent_WHO = pd.read_excel('10_AS_Vent\Base_from_whom.xlsx', index_col=0)

NBV_Vent_TOT = pd.read_excel('11_EBE_Vent\Base_Total.xlsx', index_col=0)
NBV_Vent_Pat = pd.read_excel('11_EBE_Vent\Base_Total_Pat.xlsx', index_col=0)
NBV_Vent_HCW = pd.read_excel('11_EBE_Vent\Base_Total_HCW.xlsx', index_col=0)
NBV_Vent_WHO = pd.read_excel('11_EBE_Vent\Base_from_whom.xlsx', index_col=0)

AS_NBV_Vent_TOT = pd.read_excel('12_AS_EBE_Vent\Base_Total.xlsx', 
                                index_col=0)
AS_NBV_Vent_Pat = pd.read_excel('12_AS_EBE_Vent\Base_Total_Pat.xlsx', 
                                index_col=0)
AS_NBV_Vent_HCW = pd.read_excel('12_AS_EBE_Vent\Base_Total_HCW.xlsx', 
                                index_col=0)
AS_NBV_Vent_WHO = pd.read_excel('12_AS_EBE_Vent\Base_from_whom.xlsx', 
                                index_col=0)

Base_TOT = Base_case_TOT['Total_inf']
Curt_TOT = Curtains_TOT['Total_inf']
Vent_TOT = Ventilat_TOT['Total_inf']
V_Cu_TOT = Vet_Curt_TOT['Total_inf']
NB_TOT = NB_max_TOT['Total_inf']
N_VC_TOT = FFP_TOT['Total_inf']
scre_TOT = screenin_TOT['Total_inf']
NB_sppit = NB_sppit_TOT['Total_inf']
NB_vol = NB_volm_TOT['Total_inf']
AS_TOT = AS_Vent_TOT['Total_inf']
NBV_TOT = NBV_Vent_TOT['Total_inf']
A_NB_TOT = AS_NBV_Vent_TOT['Total_inf']

Base_TOT_P = Base_case_Pat['Total_inf_P']
Curt_TOT_P = Curtains_Pat['Total_inf_P']
Vent_TOT_P = Ventilat_Pat['Total_inf_P']
V_Cu_TOT_P = Vet_Curt_Pat['Total_inf_P']
N_VC_TOT_P = FFP_Pat['Total_inf_P']
scre_TOT_P = screenin_Pat['Total_inf_P']
NB_TOT_P = NB_max_Pat['Total_inf_P']
NB_sppit_P = NB_sppit_Pat['Total_inf_P']
NB_volum_P = NB_volm_Pat['Total_inf_P']
AS_TOT_P = AS_Vent_Pat['Total_inf_P']
NBV_TOT_P = NBV_Vent_Pat['Total_inf_P']
A_NB_TOT_P = AS_NBV_Vent_Pat['Total_inf_P']


Base_TOT_H = Base_case_HCW['Total_inf_H']
Curt_TOT_H = Curtains_HCW['Total_inf_H']
Vent_TOT_H = Ventilat_HCW['Total_inf_H']
V_Cu_TOT_H = Vet_Curt_HCW['Total_inf_H']
N_VC_TOT_H = FFP_HCW['Total_inf_H']
scre_TOT_H = screenin_HCW['Total_inf_H']
NB_TOT_H = NB_max_HCW['Total_inf_H']
NB_sppit_H = NB_sppit_HCW['Total_inf_H']
NB_volum_H = NB_volm_HCW['Total_inf_H']
AS_TOT_H = AS_Vent_HCW['Total_inf_H']
NBV_TOT_H = NBV_Vent_HCW['Total_inf_H']
A_NB_TOT_H = AS_NBV_Vent_HCW['Total_inf_H']


palettes = iter(sns.husl_palette(9))

lette = 22
labels = 17
mark_s = "6"
cols = sns.color_palette("Set2")
cols.append((0.5, 0.6 , 0.55))
cols.append((0.9, 0.6 , 0.65))
cols.append((0.5, 0.9 , 0.55))
cols.append((0.5, 0.8 , 0.9))


"""                     
# -----------------------------      FIGURES      ----------------------------

    Totals for each scenario (Patients + HCWs)

"""  
names = ['Base\n Case', 
          'FP', 
          'AS',
          'HS',
          'EBS',
          'EBE',
          'Vent', 
          'HS + AS', 
          'FP +\nVent', 
          'AS +\nVent',
          'EBE +\nVent',
          'AS + EBE\n+ Vent']

f, ax3 = plt.subplots(figsize=(17,6), facecolor='w', edgecolor='k')
# ax3.set_yscale("log")
plt.rc('xtick', labelsize = labels) 
plt.ylabel('Total number of newly infected\n individuals (patients + HCW)', 
           fontsize = labels +2,
           fontname="Arial")
plt.rc('ytick', labelsize = 17) 


sns.boxplot(data=[
        Base_TOT, 
        Curt_TOT, 
        N_VC_TOT, 
        NB_TOT, 
        NB_sppit, 
        NB_vol,
        Vent_TOT, 
        scre_TOT, 
        V_Cu_TOT, 
        AS_TOT,
        NBV_TOT, 
        A_NB_TOT], 
        palette = cols,
        # palette="Set3",
        # Vent_TOT, V_Cu_TOT], palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})   
# plt.xticks(np.arange(12), names, rotation = 35) 
plt.xticks(np.arange(12), names, fontname="Arial") 
plt.ylim(top=60) 

# plt.savefig('figures/1_Figs_tests/total_general.svg', format='svg', 
#             dpi=1400)


"""                     
# -----------------------------      FIGURES      ----------------------------

    Totals for each scenario (Patients)

"""  

f, ax7 = plt.subplots(figsize=(17,6), facecolor='w', edgecolor='k')
plt.rc('xtick', labelsize = labels) 
plt.ylabel('Total number of newly\n infected patients', fontsize = labels +1,
           fontname="Arial")
plt.rc('ytick', labelsize = 17) 
sns.boxplot(data=[
                Base_TOT_P, 
                Curt_TOT_P, 
                N_VC_TOT_P, 
                NB_TOT_P, 
                NB_sppit_P,
                NB_volum_P,
                Vent_TOT_P,
                scre_TOT_P,
                V_Cu_TOT_P, 
                AS_TOT_P, 
                NBV_TOT_P, 
                A_NB_TOT_P], 

    # palette = "Set3",
    # V_Cu_TOT_P], 
    palette = cols,
      showmeans = True, showfliers=False,
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})  
plt.xticks(np.arange(12), names) 
plt.ylim(top = 20)  
# plt.savefig('figures/1_Figs_tests/totals_Pat.svg', format='svg', dpi=1400)


"""                     
# -----------------------------      FIGURES      ----------------------------

    Totals for each scenario (HCWs)

"""  
f, ax8 = plt.subplots(figsize=(17,6), facecolor='w', edgecolor='k')
plt.rc('xtick', labelsize = labels) 
plt.ylabel('Total number of newly\n infected HCWs', fontsize = labels +1,
           fontname="Arial")
plt.rc('ytick', labelsize = 17) 
# ax8.set_yscale("log") 
sns.boxplot(data=[
    Base_TOT_H, 
    Curt_TOT_H, 
    N_VC_TOT_H, 
    NB_TOT_H, 
    NB_sppit_H,
    NB_volum_H,
    Vent_TOT_H,
    scre_TOT_H, 
    V_Cu_TOT_H, 
    AS_TOT_H, 
    NBV_TOT_H, 
    A_NB_TOT_H
    ],     
    # palette = "Set3",
    # V_Cu_TOT_H], 
    palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})  
plt.xticks(np.arange(12), names) 
plt.ylim(top=60) 
# plt.savefig('figures/1_Figs_tests/totals_HCW.svg', format='svg', dpi=1400)




TOT_BC = (Base_case_TOT['Base1'] + Base_case_TOT['Base2']
+ Base_case_TOT['Base3'])
TO_Cur = Curtains_TOT['Base1'] + Curtains_TOT['Base2'] + Curtains_TOT['Base3']
TO_Ven = Ventilat_TOT['Base1'] + Ventilat_TOT['Base2'] + Ventilat_TOT['Base3']
TO_V_C = Vet_Curt_TOT['Base1'] + Vet_Curt_TOT['Base2'] + Vet_Curt_TOT['Base3']
TON_VC = FFP_TOT['Base1'] + FFP_TOT['Base2'] + FFP_TOT['Base3']
TO_scr = screenin_TOT['Base1'] + screenin_TOT['Base2'] + screenin_TOT['Base3'] 
TO_NB = NB_max_TOT['Base1'] + NB_max_TOT['Base2'] + NB_max_TOT['Base3']
TO_NBS = NB_sppit_TOT['Base1'] + NB_sppit_TOT['Base2'] + NB_sppit_TOT['Base3']
TO_NBV = NB_volm_TOT['Base1'] + NB_volm_TOT['Base2'] + NB_volm_TOT['Base3'] 
TO_ASV = AS_Vent_TOT['Base1'] + AS_Vent_TOT['Base2'] + AS_Vent_TOT['Base3']
TO_NVV = NBV_Vent_TOT['Base1'] + NBV_Vent_TOT['Base2'] + NBV_Vent_TOT['Base3']
TO_NBV = (AS_NBV_Vent_TOT['Base1'] + AS_NBV_Vent_TOT['Base2'] 
+ AS_NBV_Vent_TOT['Base3'])


HCW_BC = (Base_case_HCW['Base1'] + Base_case_HCW['Base2']
+ Base_case_HCW['Base3'])
HW_Cur = Curtains_HCW['Base1'] + Curtains_HCW['Base2'] + Curtains_HCW['Base3']
HW_Ven = Ventilat_HCW['Base1'] + Ventilat_HCW['Base2'] + Ventilat_HCW['Base3']
HW_V_C = Vet_Curt_HCW['Base1'] + Vet_Curt_HCW['Base2'] + Vet_Curt_HCW['Base3']
HW_ROM = FFP_HCW['Base1'] + FFP_HCW['Base2'] + FFP_HCW['Base3']
HW_ALL = screenin_HCW['Base1'] + screenin_HCW['Base2'] + screenin_HCW['Base3']
HW_NCM = NB_max_HCW['Base1'] + NB_max_HCW['Base2'] + NB_max_HCW['Base3']
HW_NBS = NB_sppit_HCW['Base1'] + NB_sppit_HCW['Base2'] + NB_sppit_HCW['Base3']
HW_NBV = NB_volm_HCW['Base1'] + NB_volm_HCW['Base2'] + NB_volm_HCW['Base3']
HW_ASV = AS_Vent_HCW['Base1'] + AS_Vent_HCW['Base2'] + AS_Vent_HCW['Base3']
HW_NVV = NBV_Vent_HCW['Base1'] + NBV_Vent_HCW['Base2'] + NBV_Vent_HCW['Base3']
HW_ABV = (AS_NBV_Vent_HCW['Base1'] + AS_NBV_Vent_HCW['Base2'] 
+ AS_NBV_Vent_HCW['Base3'] )


areas = ['Triage\nZone',  
          'Holding\nArea', 'Urgent\nAttention', 
          'Non-urgt\nAttention', 'Imaging',
          'POCT Lab.', 'ED Base']

plase = [5.5,  17.5, 29.5, 41.5, 53.5, 65.5, 77.5 ]


"""                     
# -----------------------------      FIGURES      ----------------------------

    Totals for each ED area (Patients + HCWs)

"""  
f, ax4 = plt.subplots(figsize=(19,6), facecolor='w', edgecolor='k')
sns.boxplot(data=[
    
                  
    Base_case_TOT['Triag'], 
    Curtains_TOT['Triag'],
    FFP_TOT['Triag'], 
    NB_max_TOT['Triag'], 
    NB_sppit_TOT['Triag'],
    NB_volm_TOT['Triag'],
    Ventilat_TOT['Triag'],  
    screenin_TOT['Triag'], 
    Vet_Curt_TOT['Triag'], 
    AS_Vent_TOT['Triag'],
    NBV_Vent_TOT['Triag'],
    AS_NBV_Vent_TOT['Triag'],
                    
                  
    Base_case_TOT['WaitN'], 
    Curtains_TOT['WaitN'],
    FFP_TOT['WaitN'], 
    NB_max_TOT['WaitN'],
    NB_sppit_TOT['WaitN'],
    NB_volm_TOT['WaitN'],
    Ventilat_TOT['WaitN'],  
    screenin_TOT['WaitN'], 
    Vet_Curt_TOT['WaitN'], 
    AS_Vent_TOT['WaitN'],
    NBV_Vent_TOT['WaitN'],
    AS_NBV_Vent_TOT['WaitN'],
                  
    Base_case_TOT['AtteU'], 
    Curtains_TOT['AtteU'],
    FFP_TOT['AtteU'], 
    NB_max_TOT['AtteU'],
    NB_sppit_TOT['AtteU'],
    NB_volm_TOT['AtteU'],
    Ventilat_TOT['AtteU'],  
    screenin_TOT['AtteU'], 
    Vet_Curt_TOT['AtteU'], 
    AS_Vent_TOT['AtteU'],
    NBV_Vent_TOT['AtteU'],
    AS_NBV_Vent_TOT['AtteU'],

                   
    Base_case_TOT['AtteN'], 
    Curtains_TOT['AtteN'],
    FFP_TOT['AtteN'], 
    NB_max_TOT['AtteN'],
    NB_sppit_TOT['AtteN'],
    NB_volm_TOT['AtteN'],
    Ventilat_TOT['AtteN'],  
    screenin_TOT['AtteN'],
    Vet_Curt_TOT['AtteN'], 
    AS_Vent_TOT['AtteN'],
    NBV_Vent_TOT['AtteN'],
    AS_NBV_Vent_TOT['AtteN'],
                  
    
    Base_case_TOT['Imagi'], 
    Curtains_TOT['Imagi'],
    FFP_TOT['Imagi'],
    NB_max_TOT['Imagi'],
    NB_sppit_TOT['Imagi'],
    NB_volm_TOT['Imagi'],
    Ventilat_TOT['Imagi'],  
    screenin_TOT['Imagi'], 
    Vet_Curt_TOT['Imagi'], 
    AS_Vent_TOT['Imagi'],
    NBV_Vent_TOT['Imagi'],
    AS_NBV_Vent_TOT['Imagi'],
                  
    Base_case_TOT['Labot'], 
    Curtains_TOT['Labot'],
    FFP_TOT['Labot'], 
    NB_max_TOT['Labot'],
    NB_sppit_TOT['Labot'],
    NB_volm_TOT['Labot'],
    Ventilat_TOT['Labot'],  
    screenin_TOT['Labot'], 
    Vet_Curt_TOT['Labot'], 
    AS_Vent_TOT['Labot'],
    NBV_Vent_TOT['Labot'],
    AS_NBV_Vent_TOT['Labot'],
    
    
    HCW_BC, 
    HW_Cur, 
    HW_ROM,  
    HW_NCM, 
    HW_NBS, 
    HW_NBV,
    HW_Ven, 
    HW_ALL,
    HW_V_C, 
    HW_ASV, HW_NVV, HW_ABV,

                  ], 
    palette = cols,
    # palette="Set3", 
    showfliers = False,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s}) 
plt.xticks(plase, areas, fontsize=16) 
plt.ylabel('Total number of newly infected\n individuals (patients + HCW)', 
           fontsize = labels +2)
plt.ylim(top=28) 
# plt.savefig('figures/1_Figs_tests/areas_total.svg', format='svg', dpi=1400)
#------------------------------------------------------------


#------------------------------------------------------------
"""                     
# -----------------------------      FIGURES      ----------------------------

    Totals for each ED area (Patients)

"""  

areas = ['Holding\nArea', 'Urgent\nAttention', 
          'Non-urgent\nAttention']
plase = [5.5,  17.5, 29.5]
f, ax3 = plt.subplots(figsize=(19,6), facecolor='w', edgecolor='k')
sns.boxplot(data=[
                  
    Base_case_Pat['WaitN_P'], 
    Curtains_Pat['WaitN_P'],
    FFP_Pat['WaitN_P'],
    NB_max_Pat['WaitN_P'],
    NB_sppit_Pat['WaitN_P'],
    NB_volm_Pat['WaitN_P'],
    Ventilat_Pat['WaitN_P'],  
    screenin_Pat['WaitN_P'],
    Vet_Curt_Pat['WaitN_P'],
    AS_Vent_Pat['WaitN_P'],
    NBV_Vent_Pat['WaitN_P'],
    AS_NBV_Vent_Pat['WaitN_P'],
                  
    Base_case_Pat['AtteU_P'], 
    Curtains_Pat['AtteU_P'],
    FFP_Pat['AtteU_P'], 
    NB_max_Pat['AtteU_P'],
    NB_sppit_Pat['AtteU_P'],
    NB_volm_Pat['AtteU_P'],
    Ventilat_Pat['AtteU_P'],
    screenin_Pat['AtteU_P'],
    Vet_Curt_Pat['AtteU_P'], 
    AS_Vent_Pat['AtteU_P'],
    NBV_Vent_Pat['AtteU_P'],
    AS_NBV_Vent_Pat['AtteU_P'],
                   
    Base_case_Pat['AtteN_P'], 
    Curtains_Pat['AtteN_P'],
    FFP_Pat['AtteN_P'],  
    NB_max_Pat['AtteN_P'], 
    NB_sppit_Pat['AtteN_P'],
    NB_volm_Pat['AtteN_P'],
    Ventilat_Pat['AtteN_P'],  
    screenin_Pat['AtteN_P'],
    Vet_Curt_Pat['AtteN_P'], 
    AS_Vent_Pat['AtteN_P'],
    NBV_Vent_Pat['AtteN_P'],
    AS_NBV_Vent_Pat['AtteN_P'],
                  
   
                  ], 
    palette = cols ,
      showmeans = True, 
      showfliers = False,
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s}) 
plt.xticks(plase, areas, fontsize = 16)
plt.ylabel('Total number of newly\n infected patients', 
           fontname="Arial", fontsize = labels +2)
plt.ylim(top = 9)
plt.savefig('figures/1_Figs_tests/areas_total_pat.svg', 
            format='svg', dpi=1400)


"""                     
# -----------------------------      FIGURES      ----------------------------

    Totals for each ED area (HCWs)

"""  

areas2 = ['Urgent\nAttention', 
          'Non-urgent\nAttention', 'Imaging', 'POCT Lab.', 
          'ED Base']
plase = [5.5,  17.5, 29.5, 41.5, 53.5]
f, ax5 = plt.subplots(figsize=(19,6), facecolor='w', edgecolor='k')
sns.boxplot(data=[
    
                  
    Base_case_HCW['AtteU_H'], 
    Curtains_HCW['AtteU_H'],
    FFP_HCW['AtteU_H'], 
    NB_max_HCW['AtteU_H'], 
    NB_sppit_HCW['AtteU_H'],
    NB_volm_HCW['AtteU_H'],
    Ventilat_HCW['AtteU_H'],  
    screenin_HCW['AtteU_H'],
    Vet_Curt_HCW['AtteU_H'],  
    AS_Vent_HCW['AtteU_H'],
    NBV_Vent_HCW['AtteU_H'],
    AS_NBV_Vent_HCW['AtteU_H'],
                   
    Base_case_HCW['AtteN_H'], 
    Curtains_HCW['AtteN_H'],
    FFP_HCW['AtteN_H'],  
    NB_max_HCW['AtteN_H'], 
    NB_sppit_HCW['AtteN_H'],
    NB_volm_HCW['AtteN_H'],
    Ventilat_HCW['AtteN_H'],  
    screenin_HCW['AtteN_H'],
    Vet_Curt_HCW['AtteN_H'], 
    AS_Vent_HCW['AtteN_H'],
    NBV_Vent_HCW['AtteN_H'],
    AS_NBV_Vent_HCW['AtteN_H'],
                  
    Base_case_HCW['Imagi_H'], 
    Curtains_HCW['Imagi_H'],
    FFP_HCW['Imagi_H'], 
    NB_max_HCW['Imagi_H'], 
    NB_sppit_HCW['Imagi_H'],
    NB_volm_HCW['Imagi_H'],
    Ventilat_HCW['Imagi_H'],  
    screenin_HCW['Imagi_H'],
    Vet_Curt_HCW['Imagi_H'],  
    AS_Vent_HCW['Imagi_H'],
    NBV_Vent_HCW['Imagi_H'],
    AS_NBV_Vent_HCW['Imagi_H'],
                  
    Base_case_HCW['Labot_H'], 
    Curtains_HCW['Labot_H'],
    FFP_HCW['Labot_H'],  
    NB_max_HCW['Labot_H'], 
    NB_sppit_HCW['Labot_H'],
    NB_volm_HCW['Labot_H'],
    Ventilat_HCW['Labot_H'],  
    screenin_HCW['Labot_H'],
    Vet_Curt_HCW['Labot_H'], 
    AS_Vent_HCW['Labot_H'],
    NBV_Vent_HCW['Labot_H'],
    AS_NBV_Vent_HCW['Labot_H'],
    
   
    HCW_BC, 
    HW_Cur, 
    HW_ROM, 
    HW_NCM,
    HW_NBS, 
    HW_NBV,
    HW_Ven, 
    HW_ALL,
    HW_V_C,
    HW_ASV, 
    HW_NVV, 
    HW_ABV,
                  ],  
    palette = cols,
      showmeans = True, 
      showfliers = False,
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s}) 
plt.xticks(plase, areas2, fontsize=16)
plt.ylabel('Total number of newly\n infected HCWs', fontsize = labels +2)
# plt.ylim(top=30) 
plt.ylim(top=28)
# plt.savefig('figures/1_Figs_tests/areas_total_HCW.svg', 
#             format='svg', dpi=1400)


