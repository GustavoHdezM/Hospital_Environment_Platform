# -*- coding: utf-8 -*-
"""
Created on Thu May 27 2021
    
    Architectural interventions to mitigate the spread of
    SARS-CoV-2 in emergency departments
    
    InnoBRI project 
    This work was supported by the Innovation Funds of the 
    Joint Federal Committee 
    (Innovationsfonds des gemeinsamen Bundesausschusses (G-BA),
     funding reference: 01VSF19032)
    
    Main file for running platform
    
@author: Gustavo Hernandez Mejia

"""
from funct_architect_interv_ED import *
import random
import matplotlib.pyplot as plt
import math  
import time
import numpy as np
import pandas as pd
import csv
import collections, numpy
import seaborn as sns

prop_cycle = plt.rcParams['axes.prop_cycle'] # Colors
colors = prop_cycle.by_key()['color']
   
"""---------------------------------------------------------------------------             
                    Users of emergency department 
                             VARIABLES                 
"""

global Users, V_recep, V_triag, V_nurse_No_Urg, dr_No_Urg_V
global V_nurse_Urg, V_dr_Urg, V_imagin, V_labor, med_test, back_lab, back_time
global invasiv_prob, neg_press_prob
global PB_RECE, P_TRI_R, P_WAT_N, P_WAT_U, P_N_URE, PB_URGE, PB_LABO 
global PB_IMAG,PB_ARE_test,PB_SYMPTOMS
global ISOLA_R, SHOCK_R, INVASIV, NEGATIV
global Own_Arrive, Suspicion_of_infection, Isolation_needed, Time_scale
global User_track_1, Seat_map, day_current, day
global N_new_day_from_shift_1,N_new_day_from_shift_2, N_new_day_from_shift_3
global Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3
global RECEP, TRIAG, TRIAG, WAI_N, WAI_U,  N_URG, U_URG,IMAGI, LABOR,EXIT_
global AT_UR, At_NU, Num_Aget, ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3
global ROMS_G, ROMS_G_NAM


#----------------------          ED Areas       -------------------------------

#----  TRIAGE and Administration areas
RECEP = 'RECEPTION'
TRIAG = 'TRIAGE'
#----  Holding Area
WAI_N = 'WAIT_NO_URGENT'  # In the code, area found as waiting area
WAI_U = 'WAIT_URGENT'     # Only state, not time inserted

#----  Emergency Rooms
N_URG = 'NOT_URGENT'
U_URG = 'URGENT'
AT_UR = 'ATTEN_URGE'
At_NU = 'ATTE_N_URG'
#---- Procedures outside the ED e.g. imaging
IMAGI = 'IMAGING'
LABOR = 'LABORATORY'
#---- Exit after completing ED services
EXIT_ = 'EXIT'
#---- ED Base
HCW_B = 'HCW_BASE'
#----------------------          ED Areas   - close   -------------------------

#----------------------       Agents Labels (status)    -----------------------
UNDEF = 'UNDEFINED'
ISOLA = 'ISOLATION_ROOM'
SHOCK = 'SHOCK_ROOM'
INVAS = 'INVASIVE_INTERVENTION_ROOM'
NEGAT = 'NEGATIVE_PRESSURE_ROOM'

INFEC = 'INFECTED'
PATIEN = 'PATIENT'
N_URGE = 'N_URGENT'
N_N_URG = 'N_N_URGE'
DR_URGE = 'DR_URGEN'
D_N_URG = 'DR_N_URGE'

SYMP_YES = 'SYMPTOM_YES'
SYMP_NO = 'SYMPTOM_NO'
REPLACE= 'ALREADY REPLACED'
DAY_SPECIFIC = "Day_spec_infec"
#----------------------       Agents Labels (status) - close    ---------------


"""----------------------------------------------------------------------------
                            ARRIVAL DATA 
                            
    Arrival data following incoming patients
    AKTIN-project. Das AKTIN-Notaufnahmeregister
    Available from: https://www.aktin.org.
"""
Df = pd.read_excel (r'data_arriv\Arriving_data.xlsx',sheet_name = None)
Aget_day = Df['Total']

# WK_cases = [3, 26, 2, 1]
# WK_cases = [2, 3, 26, 2]
WK_cases = [2, 3, 26, 2]
WK_7days = 7
WK_8days = 8
WK_1 = np.random.randint(1,WK_7days, size=(WK_cases[0]) )
WK_2 = np.random.randint(1,WK_8days, size=(WK_cases[1]) )
WK_3 = np.random.randint(1,WK_8days, size=(WK_cases[2]) )
WK_4 = np.random.randint(1,WK_7days, size=(WK_cases[3]) )

WK_1_cases = []
for i in range(WK_7days):
    WK_1_cases.append( collections.Counter(WK_1)[i]  )

WK_2_cases = []
for i in range(WK_8days):
    WK_2_cases.append( collections.Counter(WK_2)[i]  )
    
WK_3_cases = []
for i in range(WK_8days):
    WK_3_cases.append( collections.Counter(WK_3)[i]  )

WK_4_cases = []
for i in range(WK_7days):
    WK_4_cases.append( collections.Counter(WK_4)[i]  )

day_cases = WK_1_cases + WK_2_cases + WK_3_cases + WK_4_cases


"""----------------------------------------------------------------------------
                 TRANSMISSION PROB. FOR FAR-FIELD
                           
    The file reports the transmission probability (TP) over time for 
    the far-field transmission. 
    Each sheet reports the TP for a different number of infectious 
    individuals in the area in a minute-based dynamics.

    HEADS APP: https://aerosol.ds.mpg.de/en/
"""
Tr_Pr = pd.read_excel (r'data_arriv\1_BASE_TP_Update_HEADS_May_22.xlsx',
                                                            sheet_name = None)
TP_pyth = 0.01
TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General

for i in range(len(Tr_Pr['1_Reception'])):
    Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
    Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
    Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
    Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m']=int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
    Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
    Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
    Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
    Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
    Tr_Pr['10_WAIT_INTRV'].loc[i,'m']  = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
    Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(
                                           Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
    

"""----------------------------------------------------------------------------
                 TRANSMISSION PROB. FOR NEAR-FIELD

    Near-field TP	
    The file reports the transmission probability (TP) 
    over time for the near-field transmission. 	
    	
    m 	Minutes
    S_SP	surgical mask, speaking
    S_BR	surgical mask, breathing
    F_SP	FFP2 mask, speaking
    F_BR	FFP2 mask, breathing
    
    Bagheri G et al. An upper bound on one-to-one exposure to infectious human 
    respiratory particles. Proceedings of the National Academy of Sciences. 
    2021;118(49).

"""

Tr_Pr_NEAR = pd.read_excel (r'data_arriv\TP_ED _Near.xlsx',sheet_name = None)
TP_pyth_Near = 0.01                 
TP_pyth_Near = TP_pyth_Near* 0.052 # 0.062  Reduction General


"""--------------------------------------------------------------------------
                            TIME 
"""
h_ranges = []
hrs = 24
for i in range(hrs):
    h_ranges.append([(i*60)+1, (i+1)*60])


Num_Aget = Aget_day.loc[0, "tot"]  # Min 6
N_days = len(Aget_day)  # 30  


# A1 = int(Aget_day.iloc[day])

"""--------------------------------------------------------------------------
                            PATIENTS 
"""

day_current = 0
#                  Time scaling, MINUTES
Time_scale = 60*24*1*1*1   #  ->  minutes, hours, days, month, year
Active_Period = [1, 60*24] #  ->  5 h, 21h 

N_infected = 1   # random.randint(1,3) OPTION

Time_var = 0
med_test = 1
actual_user = 0

# time_area_HCW = 60*2
time_area_HCW = 40

time_area_HCW_Att = 20

Prop_P_H_N = 0.25
Prop_P_H_M = 0.1
Prop_P_P = 1
Prop_H_H_Recep = 40
Prop_H_H_Triag = 40
Prop_H_H_Nu_Nu = 20
Prop_H_H_MD_Nu = 10
Prop_H_H_Labor = 30
Prop_H_H_Nur_B = 30

NB_SPLIT = 0



"""----------------------------------------------------------------------------
                         OFFICIAL INTERVENTION MODEL
    
    NOTE: Comment/uncomment the code section for the scenario to test
          
    1. Flexible Partitions (FP) 
    (in the code, the intervention can be found as "curtains")
    2. Attention Area Separation (AS).
    3. Holding Area Separation (HS).
    (in the code, the intervention can be found as "waiting area separation")
    4. ED Base Separation (EBS).
    (in the code, ED Base can be found as "Nurse base")
    5. ED Base Extension (EBE).
    6. Ventilation (Vent).
    7. HS + AS
    8. FP + Vent
    9. AS + Vent
    10. EBE + Vent
    11. AS + EBE +Vent
    
@author: Gustavo Hernandez Mejia

"""

#------------------------------------------------------------------------------
#                            OFFICIAL   INTERVENTIONS
#                                  BASE CASE
#        

N_rooms_ = 6
N_beds_ = 6
# ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

ROMS_G = []
ROMS_G_NAM = []
for i in range(0, N_rooms_):
    ROMS_G.append(1)
    ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

BEDS_G = []
BEDS_G_NAM = []
for i in range(0, N_beds_):
    BEDS_G.append(1)
    BEDS_G_NAM.append('BEDS_{}'.format(i+1))


Area_1 = ROMS_G_NAM[0:3]
Area_2 = ROMS_G_NAM[3:6]

Area_1_U = BEDS_G_NAM[0:3]
Area_2_U = BEDS_G_NAM[3:6]

New_wait_URGT = 10
# WaitU_fact = 1000
New_wait_URGT_RED = 5

# -----------------  - Intervention indicators 

ATTEN_NU_INTRV = 0
Atten_intrv_fact = 0.5
ATTEN_NON_UR_ROOM_1 = 1
ATTEN_NON_UR_ROOM_2 = 1
ATTEN_NON_UR_ROOM_3 = 1


WAIT_NU_INTRV = 0
Wait_intrv_fact = 1

CURTAINS_INTRV = 0
CURTAINS = random.uniform(0.84,0.91)

VENTILA_INTRV = 0
if VENTILA_INTRV:
    Recep_venti = 0.80   # 20 % reduction
    Triag_venti = 0.75   # 25 % reduction
    WaitU_venti = 0.70   # 30 % reduction
    WaitN_venti = 0.80   # 20 % reduction
    Att_U_venti = 1
    Att_N_venti = 0.85   # 15 % reduction
    Imagi_venti = 0.90   # 10 % reduction
    Labor_venti = 1
    Nur_B_venti = 0.90   # 10 % reduction
else:
    Recep_venti = 1
    Triag_venti = 1
    WaitU_venti = 1
    WaitN_venti = 1
    Att_U_venti = 1
    Att_N_venti = 1
    Imagi_venti = 1
    Labor_venti = 1
    Nur_B_venti = 1

NB_INTER = 1
T_NB = 0.4 * NB_INTER

# HCW_BASES = 1
Att_interv = 1
# Att_NU_pro = 0.5     # start 0.5
Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected 
PB_SYMPTOMS = 1-0.41 # Proportion of asymptomatic infections among infected 

NB_SPLIT = 0
NB_ROOM = 0
HEAD_wait_NU = 1  # HEADS update
HEAD_wait_U = 1   # HEADS update
HEAD_Att_NU = 1  # HEADS update
HEAD_Att_U = 1    # HEADS update
HEAD_Imag = 1    # HEADS update
HEAD_Labor = 1     # HEADS update
# CURTAINS = random.uniform(0.84,0.91)
# VENTILAT = random.uniform(0.65,0.75)

# VENTILAT = 0.75
VENTILAT = 1
# CURTAINS = 1
# VENTILAT = 1
Recep_fact = 1 * Recep_venti
Triag_fact = 1 * Triag_venti
WaitU_fact = 1 * WaitU_venti
WaitN_fact = 1 * WaitN_venti
Att_U_fact = 1 * Att_U_venti
Att_N_fact = 1 * Att_N_venti
Imagi_fact = 1 * Imagi_venti
Labor_fact = 1 * Labor_venti
Nur_B_fact = 1 * Nur_B_venti

Mask = ['S_SP','S_BR','F_SP','F_BR']
SCREE_HCW = 0
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                           INTERVENTION  
#                    1. Flexible Partitions (FP) 

#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 1
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
#     Recep_venti = 0.80   # 20 % reduction
#     Triag_venti = 0.75   # 25 % reduction
#     WaitU_venti = 0.70   # 30 % reduction
#     WaitN_venti = 0.80   # 20 % reduction
#     Att_U_venti = 1
#     Att_N_venti = 0.85   # 15 % reduction
#     Imagi_venti = 0.90   # 10 % reduction
#     Labor_venti = 1
#     Nur_B_venti = 0.90   # 10 % reduction
# else:
#     Recep_venti = 1
#     Triag_venti = 1
#     WaitU_venti = 1
#     WaitN_venti = 1
#     Att_U_venti = 1
#     Att_N_venti = 1
#     Imagi_venti = 1
#     Labor_venti = 1
#     Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                                 INTERVENTION  
#                    
#                           2. Attention Area Separation (AS).
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected 

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                            OFFICIAL INTERVENTION  
#                    
#                        3.  Holding Area Separation (HS).
#        


# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 1
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected 

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                                  INTERVENTION  
#                           4. ED Base Separation (EBS).
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected 

# NB_SPLIT = 1
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0


#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                              INTERVENTION  

#                       5.   ED Base Extension (EBE).
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected 

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                             INTERVENTION  
#                          6. Ventilation (Vent)
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected 

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                            OFFICIAL INTERVENTION  
#    
#                              7.  HS + AS
#      
  
# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 1
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                                INTERVENTION  

#                              8.   FP + Vent
#        


# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 1
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                              INTERVENTION  

#                             9.  AS + Vent
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                              INTERVENTION  

#                            10.  EBE + Vent
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                              INTERVENTION  

#                           11. AS + EBE + Vent
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 0.9
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


"""----------------------------------------------------------------------------
ESI classification

"""
shift_1 = [1, 60*(8)] # ->  6 h, 14 h 
shift_2 = [(60*(8))+1, 60*(8+8)]
shift_3 = [(60*(8+8))+1, (60*(8*3))-1]

color_wait = ['YELLLOW','GREEN','BLUE']  


t_arriv = []
for i in range(hrs):
    pati = int(Df['D'+str(1)].loc[i, "DAY"])
    if pati > 0:
        for k in range(pati):
            t_ar = random.randint(h_ranges[i][0], h_ranges[i][1])   
            t_arriv.append(t_ar)
            t_arriv.sort()
            
color = ['RED','ORANGE','YELLLOW','GREEN','BLUE','WITHOUT']            
triag_pat = []
for i in range(hrs):
    for k in range(len(color)):
        if (Df['D'+str(1)].loc[i,color[k]]) > 0:
            for qq in range(Df['D'+str(1)].loc[i,color[k]]):
                if ('WITHOUT' == color[k]):
                    k1 = random.randint(2, 4)
                    triag_pat.append(color[k1])
                else:    
                    triag_pat.append(color[k])
                
            

#------           USERS (patients)
Users = []
# for i in range(Num_Aget):
for i in range(Aget_day.loc[0, "tot"]):
# User -> Agent_Number, Infection Status, Area, Area-Time, Area-time_count, arriv, 
# interact_moment, side_time, side_label, area of getting infected?, day, 
# symptom, indicate staff on shift
# ESI Red - Blue
# 15: ROOM to be in in case of attention non-urgent
    Users.append([i+1, 0, UNDEF, 0, 0, t_arriv[i],0, 0, UNDEF, UNDEF, 0, 
                           UNDEF, triag_pat[i], UNDEF, UNDEF, UNDEF])

User_track_1 = []



"""                            WORKERS (HCW)
                               
                 Number of HCW according to UMG data 
                               
"""
#                 SET THE NUMBER OF WORKERS PER AREA AND SHIFT (s1-s3)
recep_N_s1 = 3
recep_N_s2 = 2
recep_N_s3 = 1

triag_N_s1 = 2
triag_N_s2 = 2
triag_N_s3 = 1

triag_U_N_s1 = 2
triag_U_N_s2 = 1
triag_U_N_s3 = 1

nur_NU_N_s1 = 4
nur_NU_N_s2 = 4
nur_NU_N_s3 = 3

Dr_NU_s1 = 4
Dr_NU_s2 = 4
Dr_NU_s3 = 3
# nurs_U_N = 2
# # Dr_NU_N = 1
# Dr_Ur_N = 1

imagi_N = 2
labor_N = 1

"""----------------------------------------------------------------------------
                         WORKERS DEFINITIONS
    
                    Characteristics per ED Area

"""
V_recep_1 = []
V_recep_2 = []
V_recep_3 = []
for i in range(recep_N_s1):
    V_recep_1.append([i, 0, RECEP, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
for i in range(recep_N_s2):
    V_recep_2.append([i, 0, RECEP, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
for i in range(recep_N_s3):
    V_recep_3.append([i, 0, RECEP, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])


"""                  Worker TRIAGE/REGIS
"""
V_triag_1 = []
V_triag_2 = []
V_triag_3 = []
for i in range(triag_N_s1):
    V_triag_1.append([i, 0, TRIAG, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
for i in range(triag_N_s2):
    V_triag_2.append([i, 0, TRIAG, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
for i in range(triag_N_s3):
    V_triag_3.append([i, 0, TRIAG, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    

"""                 Worker NO URGENT and URGENT (TOGETHER UMG FEEDBACK)
"""

# 16 - Indication of rooms for Non-Urgent area
# 17 - Indication of bed for Urgent area
# 18 - Indication of rooms 2 for Non-Urgent area
# 19 - Indication of bed 2 for Urgent area
V_nurse_No_Urg_1 = []
V_nurse_No_Urg_2 = []
V_nurse_No_Urg_3 = []
    
for i in range(nur_NU_N_s1):
    V_nurse_No_Urg_1.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
                             0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                             , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                             , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
for i in range(nur_NU_N_s2):
    V_nurse_No_Urg_2.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
                             0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                             , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                             , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
for i in range(nur_NU_N_s3):
    V_nurse_No_Urg_3.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
                             0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                             , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                             , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
    


# 16 - Indication of rooms for Non-Urgent area
# 17 - Indication of bed for Urgent area    

# 18 - Indication of rooms 2 for Non-Urgent area
# 19 - Indication of bed 2 for Urgent area
dr_No_Urg_V_1 = []
dr_No_Urg_V_2 = []
dr_No_Urg_V_3 = []

for i in range(Dr_NU_s1):
    dr_No_Urg_V_1.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
                          UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                          , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                          , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
for i in range(Dr_NU_s2):
    dr_No_Urg_V_2.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
                          UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                          , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                          , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
for i in range(Dr_NU_s3):
    dr_No_Urg_V_3.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
                          UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                          , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                          , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])

"""                  Worker IMAGING
"""
V_imagin_1 = []
V_imagin_2 = []
V_imagin_3 = []
for i in range(imagi_N):
    V_imagin_1.append([i, 0, IMAGI, 0, 0, UNDEF, 0,
                       UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_imagin_2.append([i, 0, IMAGI, 0, 0, UNDEF, 0,
                       UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_imagin_3.append([i, 0, IMAGI, 0, 0, UNDEF, 0,
                       UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])


"""                  Worker LABORATORY
"""
V_labor_1 = []
V_labor_2 = []
V_labor_3 = []
for i in range(labor_N):
    V_labor_1.append([i, 0, LABOR, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_labor_2.append([i, 0, LABOR, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_labor_3.append([i, 0, LABOR, 0, 0, UNDEF, 0,
                      UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    

"""---------------------------------------------------------------------------
        Time of stay per area
        Time according to UMG data - Dr. Blaschke
        
""" 
RECEP_t_1   = [5, 10]          # 5 - 10min 
# TRIAG_U_t_1 = [5, 10]        # 5 - 10min 
t_triage_1  = [5, 10]          # 5 - 10min 
# t_wait_Nu_1 = [10, 60*4]     # 10 - 4h 
# t_wait_Ur_1 = [2, 10]        # 2 - 10 min   # ORANGE
t_Urgent_1  = [60*2, 60*4]     # 2h - 4h 
t_N_Urgen_1 = [60*1, 60*6]     # 4h - 6h 

t_wait_Nu_1 = [30, 60, 120]    # ESI 3: up to 30, ES 4: up to 60, ESI 5: to 120
t_wait_Ur_1 = [1, 10]          # 2 - 10 min   # ESI ORANGE
"""---------------------------------------------------------------------------
"""    


"""---------------------  ROOMS in ATTENTION NON-URGENT AREA   ----------------
"""
# # ROOM availeable = 1
# # ROOM  occupied  = 0
# #  Init with all rooms availeable
# ATT_NU_ROOM_1 = 1
# ATT_NU_ROOM_2 = 1
# ATT_NU_ROOM_3 = 1



"""---------------------------------------------------------------------------
              
                  PATHOGEN TRANSMISSION PROBABILITY (RISK)
"""
#           Probability based on risk and pathogen transmission
# low = 0.20          # 20% probability
# medium = 0.45       # 45% probability
# high = 0.75         # 75% probability
# very_high = 0.9     # 90% probability

# # Risk per ED area
# PB_RECE = low
# P_TRI_R = medium
# P_TRI_U = high
# P_WAT_N = high   # Outpatients
# P_WAT_U = high   # Urgent patients
# P_N_URE = medium
# PB_URGE = medium
# PB_LABO = low
# PB_IMAG = low
# PB_ARE_test = medium

# # Risk on potential interventions
# ISOLA_R = very_high
# SHOCK_R = very_high
# INVASIV = very_high
# NEGATIV = medium

"""---------------------------------------------------------------------------
""" 

#                   Probabiliies for desitions and flow

Medic_test = 0.5                # confirmed UMG

# Own_Arrive = 0.6                # confirmed UMG
# Suspicion_of_infection = 0.2
# Isolation_needed = 0.2          # confirmed UMG (0.1 - 0.3)
# invasiv_prob = 0.15
# neg_press_prob = 0.15

# Isolation_room = 0            
# Emergen_doct = 1
# Shock_room = 0
# roll_up_wall = 0
# Invasiv_room = 0
# negt_pres_room = 0
# emerg_doctor = 0


"""------------------Seat Map Waiting Area  -----------------------------------
"""
Seat_map = np.zeros((4,10))
Seat_map = Seat_map.astype(int)

"""---------------------------------------------------------------------------
""" 



"""----------------------------------------------------------------------------
                         ARRIVAL TO EMERGENCY DEPARTMENT
"""

def arrival_method(tim):
    # Time_var = tim
    
    # for j in range(Num_Aget):
    for j in range(len(Users)):
        ESI = Users[j][12]
        if color[0] == ESI:         # RED               (NO WAITING)
            Users[j][2] = AT_UR     # ATTENTION URGENT 
            t_Urgent = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[j][3] = t_Urgent
            Users[j][4] = 0
            # Users[j][6] = random.randint(1, t_Urgent)
            
        elif color[1] == ESI:       # ORANGE            (1- 10 MIN WAITING)
            Users[j][2] = WAI_U     # WAITING URGENT 
            t_wait_Ur = random.randint(t_wait_Ur_1[0], t_wait_Ur_1[1])
            Users[j][3] = t_wait_Ur
            Users[j][4] = 0
            # Users[j][6] = random.randint(1, t_wait_Ur)
            
            
        else:                       # YELLOW - GREEN - BLUE 
            Users[j][2] = RECEP     # RECEPTION 
            RECEP_t = random.randint(RECEP_t_1[0], RECEP_t_1[1])
            Users[j][3] = RECEP_t
            Users[j][4] = 0
            # Users[j][6] = random.randint(1, RECEP_t)

    return

"""----------------------------------------------------------------------------
                     FLOW PER POSSIBLE AREAS OF DEPARTMENT
"""

def area_desit_tree(agent, i):   
#    day = da        
    Curr_Area = agent[2]
    
    if RECEP == Curr_Area:
        Next_Area = TRIAG
        Users[i][2] = Next_Area
        t_triage = random.randint(t_triage_1[0], t_triage_1[1])
        Users[i][3] = t_triage
        Users[i][4] = 0
        # Users[i][6] = random.randint(1, t_triage)
        
    if  TRIAG == Curr_Area:
        Next_Area = WAI_N
        Users[i][2] = Next_Area
        for k in range(len(color_wait)):
            if color_wait[k] == agent[12]:
                # tim = t_wait_Nu_1[k]
                t_wait_Nu = random.randint(2, t_wait_Nu_1[k])
        Users[i][3] = t_wait_Nu
        Users[i][4] = 0
        # Users[i][6] = random.randint(1, t_wait_Nu)    
        
    if WAI_U == Curr_Area:

        #   ----------     INTERVENTIONS INIT  -------------------
        #  --  Having three beds in the general urgent area
        if (BEDS_G[0] == 1):
            Next_Area = AT_UR  # N_URG
            Users[i][2] = Next_Area
            t_N_Urgen = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[i][3] = t_N_Urgen
            Users[i][4] = 0
            Users[i][15] = BEDS_G_NAM[0]
            ATT_NU_ROOM_1 = 0
            BEDS_G[0] = ATT_NU_ROOM_1
            # ATT_NU_ROOM_1 = 0
        elif (BEDS_G[1] == 1):
            Next_Area = AT_UR  # N_URG
            Users[i][2] = Next_Area
            t_N_Urgen = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[i][3] = t_N_Urgen
            Users[i][4] = 0
            Users[i][15] = BEDS_G_NAM[1]
            ATT_NU_ROOM_2= 0
            BEDS_G[1] = ATT_NU_ROOM_2
            # ATT_NU_ROOM_2 = 0
        elif BEDS_G[2] == 1:
            Next_Area = AT_UR  # N_URG
            Users[i][2] = Next_Area
            t_N_Urgen = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[i][3] = t_N_Urgen
            Users[i][4] = 0
            Users[i][15] = BEDS_G_NAM[2]
            ATT_NU_ROOM_3 = 0 
            BEDS_G[2] = ATT_NU_ROOM_3
            # ATT_NU_ROOM_3 = 0
        elif (BEDS_G[0] == 0 and BEDS_G[1] == 0 and BEDS_G[2] == 0):
            #  IF all beds occupied, send back to waiting area for N time
            TR_1 = 0
            TR_2 = 0
            TR_3 = 0
            for k in range(len(Users)):
                if (( Users[k][2] == 'ATTEN_URGE' ) and
                    (Users[k][15] == BEDS_G_NAM[0]) ):
                    TR_1 = Users[k][3] - Users[k][4]
                    
                if (( Users[k][2] == 'ATTEN_URGE' ) and
                    (Users[k][15] == BEDS_G_NAM[1] ) ):
                    TR_2 = Users[k][3] - Users[k][4]
                    
                if (( Users[k][2] == 'ATTEN_URGE' ) and
                    (Users[k][15] == BEDS_G_NAM[2] ) ):
                    TR_3 = Users[k][3] - Users[k][4]
                  
            T_new = min(TR_1,TR_2,TR_3)
            if T_new == 0:
                T_new = New_wait_URGT
            Next_Area = WAI_U
            Users[i][2] = Next_Area
            t_wait_Nu = random.randint(1, T_new)
            if color[0] == Users[i][12]:  # ESI in RED, wait up to 5 min
                T_new = New_wait_URGT_RED
                t_wait_Nu = random.randint(1, T_new)
            Users[i][3] = t_wait_Nu
            Users[i][4] = 0

        #   ----------     INTERVENTIONS CLOSE  -------------------
        
        
    if WAI_N == Curr_Area:
        
        if WAIT_NU_INTRV:
            # print(ATTEN_NU_INTRV)
            # Check room availeability
            
            # ROMS_G_NAM
            # ROMS_G
            # for i in range(len(ROMS_G)):
            
            if (ROMS_G[0] == 1):
                Next_Area = At_NU  # N_URG
                Users[i][2] = Next_Area
                t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                Users[i][3] = t_N_Urgen
                Users[i][4] = 0
                Users[i][15] = ROMS_G_NAM[0]
                ATT_NU_ROOM_1 = 0
                ROMS_G[0] = ATT_NU_ROOM_1
                # ATT_NU_ROOM_1 = 0
            elif (ROMS_G[1] == 1):
                Next_Area = At_NU  # N_URG
                Users[i][2] = Next_Area
                t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                Users[i][3] = t_N_Urgen
                Users[i][4] = 0
                Users[i][15] = ROMS_G_NAM[1]
                ATT_NU_ROOM_2= 0
                ROMS_G[1] = ATT_NU_ROOM_2
                # ATT_NU_ROOM_2 = 0
            elif ROMS_G[2] == 1:
                Next_Area = At_NU  # N_URG
                Users[i][2] = Next_Area
                t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                Users[i][3] = t_N_Urgen
                Users[i][4] = 0
                Users[i][15] = ROMS_G_NAM[2]
                ATT_NU_ROOM_3 = 0 
                ROMS_G[2] = ATT_NU_ROOM_3
                # ATT_NU_ROOM_3 = 0
            elif (ROMS_G[0] == 0 and ROMS_G[1] == 0 and ROMS_G[2] == 0):
                #  IF all rooms occupied, send back to waiting area for N time
                TR_1 = 0
                TR_2 = 0
                TR_3 = 0
                for k in range(len(Users)):
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[0]) ):
                        TR_1 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[1] ) ):
                        TR_2 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[2] ) ):
                        TR_3 = Users[k][3] - Users[k][4]
                      
                T_new = min(TR_1,TR_2,TR_3)
                if T_new == 0:
                    T_new = 30
                Next_Area = WAI_N
                Users[i][2] = Next_Area
                t_wait_Nu = random.randint(1, T_new)
                Users[i][3] = t_wait_Nu
                Users[i][4] = 0
        else:

            if (np.count_nonzero(ROMS_G) == 0):
                TR_1 = 0
                TR_2 = 0
                TR_3 = 0
                TR_4 = 0
                TR_5 = 0
                TR_6 = 0
                for k in range(len(Users)):
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[0]) ):
                        TR_1 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[1] ) ):
                        TR_2 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[2] ) ):
                        TR_3 = Users[k][3] - Users[k][4]
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[3] ) ):
                        TR_4 = Users[k][3] - Users[k][4]
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[4] ) ):
                        TR_5 = Users[k][3] - Users[k][4]
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[5] ) ):
                        TR_6 = Users[k][3] - Users[k][4]
                        
                T_new = min(TR_1,TR_2,TR_3, TR_4,TR_5,TR_6)
                if T_new == 0:     #   Patient can be sent back to waiting area
                    T_new = 30     #   for the next availeable time room or up to 30 min
                Next_Area = WAI_N
                Users[i][2] = Next_Area
                t_wait_Nu = random.randint(1, T_new)
                Users[i][3] = t_wait_Nu
                Users[i][4] = 0
                
            else:
                
                if (ROMS_G[0] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[0]
                    ATT_NU_ROOM_1 = 0
                    ROMS_G[0] = ATT_NU_ROOM_1
                    
                elif (ROMS_G[1] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[1]
                    ATT_NU_ROOM_2= 0
                    ROMS_G[1] = ATT_NU_ROOM_2
                    # ATT_NU_ROOM_2 = 0
                elif ROMS_G[2] == 1:
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[2]
                    ATT_NU_ROOM_3 = 0 
                    ROMS_G[2] = ATT_NU_ROOM_3
                # ATT_NU_ROOM_3 = 0
                
                elif (ROMS_G[3] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[3]
                    ATT_NU_ROOM_1 = 0
                    ROMS_G[3] = ATT_NU_ROOM_1
                    
                elif (ROMS_G[4] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[4]
                    ATT_NU_ROOM_2 = 0
                    ROMS_G[4] = ATT_NU_ROOM_2
                    # ATT_NU_ROOM_2 = 0
                elif ROMS_G[5] == 1:
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[5]
                    ATT_NU_ROOM_3 = 0 
                    ROMS_G[5] = ATT_NU_ROOM_3
                # ATT_NU_ROOM_3 = 0

        #----------------------------------------------------------------------
              # To unseat patient once in attention services
        #        ind = [(index, row.index(Users[i][0])) for index, 
        # row in enumerate(Seat_map) if (Users[i][0]) in row]
                # ind = np.where(Seat_map == Users[i][0])
                # Seat_map[ind[0], ind[1]] = 0
        #----------------------------------------------------------------------
        
    if (At_NU == Curr_Area or AT_UR == Curr_Area or IMAGI == Curr_Area or 
                                           LABOR == Curr_Area):

        # -------   ATTENTION NON-URGENT  INIT ------------------
        if ( Users[i][15] != UNDEF ):
            if ( Users[i][15] == ROMS_G_NAM[0] ):
                ATT_NU_ROOM_1 = 1
                ROMS_G[0] = ATT_NU_ROOM_1
            if ( Users[i][15] == ROMS_G_NAM[1] ):
                ATT_NU_ROOM_2 = 1
                ROMS_G[1] = ATT_NU_ROOM_2
            if ( Users[i][15] == ROMS_G_NAM[2] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[2] = ATT_NU_ROOM_3
            
            if ( Users[i][15] == ROMS_G_NAM[3] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[3] = ATT_NU_ROOM_3
            if ( Users[i][15] == ROMS_G_NAM[4] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[4] = ATT_NU_ROOM_3
            if ( Users[i][15] == ROMS_G_NAM[5] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[5] = ATT_NU_ROOM_3
            
        # -------   ATTENTION NON-URGENT  CLOSE ------------------
        
        # -------   ATTENTION   URGENT  INIT ------------------
        if ( Users[i][15] != UNDEF ):
            if ( Users[i][15] == BEDS_G_NAM[0] ):
                ATT_NU_ROOM_1 = 1
                BEDS_G[0] = ATT_NU_ROOM_1
            if ( Users[i][15] == BEDS_G_NAM[1] ):
                ATT_NU_ROOM_2 = 1
                BEDS_G[1] = ATT_NU_ROOM_2
            if ( Users[i][15] == BEDS_G_NAM[2] ):
                ATT_NU_ROOM_3 = 1
                BEDS_G[2] = ATT_NU_ROOM_3
        # -------   ATTENTION   URGENT  CLOSE ------------------
        
        Next_Area = EXIT_
        Users[i][2] = Next_Area
        # t_N_Urgen = random.randint(40, 2*60)
        Users[i][3] = 0
        Users[i][4] = 0
    
    return agent

"""----------------------------------------------------------------------------
                           ROUTINE SHIFT 1
"""             
def action_desit_tree(agent, i, da, currt_time):    
    Curr_Area = agent[2]
    day_current = da     
    # interact_event = agent[6]
    # current_time = agent[4]
        
    if RECEP == Curr_Area:
        # FAR - FIELD
        # Sucep patient
        #   1- Check for the number of other suscp or infect in the room, 
        #   PAT and HCWs
        #   2- if infected in the room - 
        #       -Check for the FF interaction time, the area time (agent[3])
        #       -Checks the TP for that area time, since previously known the
        #         time of other infectious ocupants
        #   3- if TP TRUE - starts infection status
        #       agent[9] = Curr_Area           (area)
        #       agent[10] = day_current + 1    (day of infection)
        #       agent[11] = PATIEN+'_RECEPTION', (if (N_of(P_inf) > 
        #
        # Infected patient
        #   1- Checks the TP for the area time for the interaction with HCWs
        #   2- if TP TRUE - starts infection status for HCWs in the area
        #

        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            P_inf = []
            P_sus = []
            H_inf = []
            H_sus = []
            
            if (agent[1] == 0):
                for i in range(len(Users)):
                    if ((Users[i][5] < currt_time) and 
                        (Users[i][2] =='RECEPTION')):
                        if(Users[i][1] == 1):
                            cont_inf = cont_inf + 1
                            P_inf.append(Users[i])
                        if(Users[i][1] == 0):  
                            cont_tot = cont_tot + 1
                            P_sus.append(Users[i])
     
                for i in range(recep_N_s1):
                    if V_recep_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                        H_inf.append(V_recep_1[i])
                    elif V_recep_1[i][1] == 0:
                        H_sus.append(V_recep_1[i])
                        
                # infected = cont_inf + cont_inf_HCW
                infected = len(P_inf) + len(H_inf)
                
                if infected > 0:
                    times_P = []
                    times_H = []
                    time_pat = 0
                    time_hcw = 0
                    A1 = Tr_Pr['1_Reception'].loc[:,'m']
                    # diff = np.absolute(A1 - exp_time)
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    TP = Tr_Pr['1_Reception'].loc[index, 
                                                  infected]*TP_pyth
                    TP = TP * Recep_fact
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        if (len(P_inf) > len(H_inf)):
                            agent[11] = PATIEN +'_RECEPTION'
                        elif (len(H_inf) >= len(P_inf)):
                            agent[11] = 'Staff1_RECEPTION'
            
            if (agent[1] == 1):   
                
                A1 = Tr_Pr['1_Reception'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['1_Reception'].loc[index, 
                                                  1]*TP_pyth
                TP = TP * Recep_fact
                
                for i in range(len(V_recep_1)):
                    if V_recep_1[i][1] == 0 and V_recep_1[i][6] == 0:
                        Trnasmiss = random.random() < TP   
                        if (Trnasmiss):
                            V_recep_1[i][3] = day_current + 1 
                            # V_recep_2[i][5] = PATIEN + '_RECEPTION'
                            V_recep_1[i][6] = day_current + 1 
                            V_recep_1[i][5] = PATIEN +'_RECEPTION'

        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            P_inf = []
            P_sus = []
            H_inf = []
            H_sus = []
            
            if (agent[1] == 0):
                for i in range(len(Users)):
                    if ((Users[i][5] < currt_time) and 
                         (Users[i][2] =='RECEPTION')):
                        if(Users[i][1] == 1):
                            cont_inf = cont_inf + 1
                            P_inf.append(Users[i])
                        if(Users[i][1] == 0):  
                            cont_tot = cont_tot + 1
                            P_sus.append(Users[i])
     
                for i in range(recep_N_s2):
                    if V_recep_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                        H_inf.append(V_recep_2[i])
                    elif V_recep_2[i][1] == 0:
                        H_sus.append(V_recep_2[i])
                        
                # infected = cont_inf + cont_inf_HCW
                infected = len(P_inf) + len(H_inf)
                
                if infected > 0:
                    times_P = []
                    times_H = []
                    time_pat = 0
                    time_hcw = 0
                    
                    A1 = Tr_Pr['1_Reception'].loc[:,'m']
                    # diff = np.absolute(A1 - exp_time)
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    TP = Tr_Pr['1_Reception'].loc[index, 
                                                  infected]*TP_pyth
                    TP = TP * Recep_fact
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff2_RECEPTION" 
                        if (len(P_inf) > len(H_inf)):
                            agent[11] = PATIEN +'_RECEPTION'
                        elif (len(H_inf) >= len(P_inf)):
                            agent[11] = 'Staff2_RECEPTION'
                
            if (agent[1] == 1):   
                
                A1 = Tr_Pr['1_Reception'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['1_Reception'].loc[index, 
                                                  1]*TP_pyth
                TP = TP * Recep_fact
                for i in range(len(V_recep_2)):
                    if V_recep_2[i][1] == 0 and V_recep_2[i][6] == 0:
                        Trnasmiss = random.random() < TP   
                        if (Trnasmiss):
                            V_recep_2[i][3] = day_current + 1 
                            # V_recep_2[i][5] = PATIEN + '_RECEPTION'
                            V_recep_2[i][6] = day_current + 1 
                            if agent[1] == 1:
                                V_recep_2[i][5] = PATIEN +'_RECEPTION'
     
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            P_inf = []
            P_sus = []
            H_inf = []
            H_sus = []
            
            if (agent[1] == 0):
                for i in range(len(Users)):
                    if ((Users[i][5] < currt_time) and 
                        (Users[i][2] =='RECEPTION')):
                        if(Users[i][1] == 1):
                            cont_inf = cont_inf + 1
                            P_inf.append(Users[i])
                        if(Users[i][1] == 0):  
                            cont_tot = cont_tot + 1
                            P_sus.append(Users[i])
     
                for i in range(recep_N_s3):
                    if V_recep_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                        H_inf.append(V_recep_3[i])
                    elif V_recep_3[i][1] == 0:
                        H_sus.append(V_recep_3[i])
                        
                # infected = cont_inf + cont_inf_HCW
                infected = len(P_inf) + len(H_inf)
                
                if infected > 0:
                    times_P = []
                    times_H = []
                    time_pat = 0
                    time_hcw = 0
                    A1 = Tr_Pr['1_Reception'].loc[:,'m']
                    # diff = np.absolute(A1 - exp_time)
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    TP = Tr_Pr['1_Reception'].loc[index, 
                                                  infected]*TP_pyth
                    TP = TP * Recep_fact
                    
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        if (len(P_inf) > len(H_inf)):
                            agent[11] = PATIEN +'_RECEPTION'
                        elif (len(H_inf) >= len(P_inf)):
                            agent[11] = 'Staff3_RECEPTION'
            
            if (agent[1] == 1):   
                
                A1 = Tr_Pr['1_Reception'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['1_Reception'].loc[index, 
                                                  1]*TP_pyth
                TP = TP * Recep_fact
                
                for i in range(len(V_recep_3)):
                    if V_recep_3[i][1] == 0 and V_recep_3[i][6] == 0:
                        Trnasmiss = random.random() < TP   
                        if (Trnasmiss):
                            V_recep_3[i][3] = day_current + 1 
                            # V_recep_2[i][5] = PATIEN + '_RECEPTION'
                            V_recep_3[i][6] = day_current + 1 
                            V_recep_3[i][5] = PATIEN +'_RECEPTION'
    
    if TRIAG == Curr_Area:
        # FAR - FIELD
        # Sucep patient
        #   1- Check for the number of other suscp or infect in the room, 
        #   2- if infected in the room - 
        #       -Check for the FF interaction time, the area time (agent[3])
        #       -Checks the TP for that area time, since previously known the 
        #        other infectious ocupants
        #   3- if TP TRUE - starts infection status
        #       agent[9] = Curr_Area           (area)
        #       agent[10] = day_current + 1    (day of infection)
        #       agent[11] = PATIEN+'_RECEPTION', (if (N_of(P_inf) 
        #
        # Infected patient
        #   1- Checks the TP for the area time for the interaction with HCWs
        #   2- if TP TRUE - starts infection status for HCWs in the area
        #

        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
 
            for i in range(triag_N_s1):
                if V_triag_1[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = cont_inf + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['2_Triage'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['2_Triage'].loc[index, infected]*TP_pyth
                TP = TP * Triag_fact
                for i in range(triag_N_s1):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and (cont_inf != 0 or cont_inf_HCW != 0)):
                        if V_triag_1[i][1] == 0 and V_triag_1[i][6] == 0:
    #                        V_recep[i][1] = 1    # Worker potential infection
                            V_triag_1[i][3] = day_current + 1 
                            # V_triag_1[i][5] = PATIEN+'_TRIAGE'
                            V_triag_1[i][6] = day_current + 1 
                            if cont_inf > cont_inf_HCW:
                                V_triag_1[i][5] = PATIEN +'_TRIAGE'
                            elif cont_inf_HCW >= cont_inf:
                                V_triag_1[i][5] = 'Staff1_TRIAGE'
                            
                
                
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff1_TRIAGE"
                    if cont_inf > cont_inf_HCW:
                        agent[11] = PATIEN +'_RECEPTION'
                    elif cont_inf_HCW >= cont_inf:
                        agent[11] = 'Staff1_TRIAGE'
            
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
 
            for i in range(triag_N_s2):
                if V_triag_2[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = cont_inf + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['2_Triage'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['2_Triage'].loc[index, infected]*TP_pyth
                TP = TP * Triag_fact
                for i in range(triag_N_s2):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and (cont_inf != 0 or cont_inf_HCW != 0)):
                        if V_triag_2[i][1] == 0 and V_triag_2[i][6] == 0:
    #                        V_recep[i][1] = 1    # Worker potential infection
                            V_triag_2[i][3] = day_current + 1 
                            V_triag_2[i][5] = PATIEN +'_TRIAGE'
                            V_triag_2[i][6] = day_current + 1 
                            if cont_inf > cont_inf_HCW:
                                V_triag_2[i][5] = PATIEN +'_TRIAGE'
                            elif cont_inf_HCW >= cont_inf:
                                V_triag_2[i][5] = 'Staff2_TRIAGE'
                
        
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff2_TRIAGE"
                    if cont_inf > cont_inf_HCW:
                        agent[11] = PATIEN +'_RECEPTION'
                    elif cont_inf_HCW >= cont_inf:
                        agent[11] = 'Staff2_TRIAGE'
            
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
 
            for i in range(triag_N_s3):
                if V_triag_3[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = cont_inf + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['2_Triage'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['2_Triage'].loc[index, 
                                           infected]*TP_pyth
                TP = TP * Triag_fact
                for i in range(triag_N_s3):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and (cont_inf != 0 or cont_inf_HCW != 0)):
                        if V_triag_3[i][1] == 0 and V_triag_3[i][6] == 0:
    #                        V_recep[i][1] = 1   # Worker potential infection
                            V_triag_3[i][3] = day_current + 1 
                            V_triag_3[i][5] = PATIEN +'_TRIAGE'
                            V_triag_3[i][6] = day_current + 1 
                            if cont_inf > cont_inf_HCW:
                                V_triag_3[i][5] = PATIEN +'_TRIAGE'
                            elif cont_inf_HCW >= cont_inf:
                                V_triag_3[i][5] = 'Staff3_TRIAGE'
                

                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff3_TRIAGE"
                    if cont_inf > cont_inf_HCW:
                        agent[11] = PATIEN +'_RECEPTION'
                    elif cont_inf_HCW >= cont_inf:
                        agent[11] = 'Staff3_TRIAGE'         
            

    if WAI_U == Curr_Area:
        
        cont_tot = 0
        cont_inf = 0

        for i in range(len(Users)):
            if (Users[i][5] < currt_time) and (Users[i][2] =='WAIT_URGENT'):
                cont_tot = cont_tot + 1
                if(Users[i][1] == 1):
                    cont_inf = cont_inf + 1
        infected = cont_inf 
        
        if infected > 0:
            A1 = Tr_Pr['4_Wait_Urg_Flur'].loc[:,'m']
            diff = np.absolute(A1 - agent[3])
            index = diff.argmin()
            TP = Tr_Pr['4_Wait_Urg_Flur'].loc[index, infected]*TP_pyth
            Ext_waitU = 300
            TP = TP * WaitU_fact*Ext_waitU*HEAD_wait_U
            # TP = TP*100
    

            Trnasmiss = random.random() < TP     
            if Trnasmiss and (agent[1] == 0):
                agent[1] = 2
                agent[9] = Curr_Area
                agent[10] = day_current + 1 
                agent[11] = "WAIT_URGENT"
            
            for i in range(len(Users)):
                if( (Users[i][5] < currt_time) and 
                   (Users[i][2] =='WAIT_URGENT') and
                    (Users[i] != agent) and
                    (Users[i][1] == 0) ):
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 1):
                        Users[i][1] = 2
                        Users[i][9] = Curr_Area
                        Users[i][10] = day_current + 1 
                        Users[i][11] = "WAIT_URGENT"

    
    if WAI_N == Curr_Area:
        # FAR - FIELD
        # Sucep patient
        #   1- Check for the number of other suscp or infect in the room, PAT 
        #   2- if infected in the room - 
        #       -Check for the FF interaction time, the area time (agent[3])
        #       -Checks the TP for that area time, since previously 
        #        known the time of other infectious ocupants
        #   3- if TP TRUE - starts infection status
        #       agent[9] = Curr_Area           (area)
        #       agent[10] = day_current + 1    (day of infection)
        #       agent[11] = (WHO?)
        #
        # Infected patient
        #   1- Checks the TP for the area time for the interaction with all 
        #       other PAt  in the area
        #   2- if TP TRUE - starts infection status for PATs in the area
        #
        # NEAR-FIELD
        #   Infected PAT
        #   1- Search for suscp PAT (random selected) - estimate interaction 
        #       time for NF TP
        #     - if TP TRUE, suscep starts infect status
        #
        # ----------------------- INTERVENTIONS ------------------------------
        # Intervention in waiting area - WAITING NON URGENT SPLIT
        # Base case: patients come to the general waiting room area and 
        # interact there following the TP in 3_Wait_NoN
        # 
        # Intervent: patients are randomly accomodated in one of two rooms, 
        # they interact there with the TP 10_WAIT_INTRV, and two major levels  
        # applied - WAT_ROM_1 or WAT_ROM_2
        # For the counting, both continue as WAIT_NO_URGENT

        if WAIT_NU_INTRV:
            # print(WAIT_NU_INTRV)
            
            #               SETTING FOR  WAT_ROM_1 
            #  --------  FAR FIELD  WAI_N ROOM 1  INIT  --------
            cont_tot = 0
            cont_inf = 0
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and 
                    (Users[i][2] =='WAIT_NO_URGENT') and 
                    (Users[i][13] =='WAT_ROM_1') ):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
            infected = cont_inf 
            
            if infected > 0:
                # A1 = Tr_Pr['3_Wait_NoN'].loc[:,'m']
                A1 = Tr_Pr['10_WAIT_INTRV'].loc[:,'m']
                
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                # TP = Tr_Pr['3_Wait_NoN'].loc[index, infected]*TP_pyth
                TP = Tr_Pr['10_WAIT_INTRV'].loc[index, infected]*(TP_pyth * 
                                                            Wait_intrv_fact)
                TP = TP * WaitN_fact
                Trnasmiss = random.random() < TP     
                if (Trnasmiss and (agent[1] == 0) and  
                    (agent[13] =='WAT_ROM_1')):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = "WAIT_NO_URGENT"
                    # print(WAIT_NU_INTRV)
                
                # for i in range(len(Users)):
                #     if( (Users[i][5] < currt_time) and 
                #        (Users[i][2] =='WAIT_NO_URGENT') and
                #         (Users[i] != agent) and
                #         (Users[i][1] == 0) and
                #         (Users[i][13] == 'WAT_ROM_1')):
                #         Trnasmiss = random.random() < TP 
                #         if Trnasmiss and (agent[1] == 1):
                #             Users[i][1] = 2
                #             Users[i][9] = Curr_Area
                #             Users[i][10] = day_current + 1 
                #             Users[i][11] = "WAIT_NO_URGENT"
                            # print(WAIT_NU_INTRV)
            #  ----------  FAR FIELD  WAI_N ROOM 1  CLOSE  --------
            #------------    NEAR FIELD  WAI_N ROOM 1  INIT  -----------------
            Sucep_Area = []
            if agent[1] == 1:
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='WAIT_NO_URGENT') and
                       (Users[i][1] == 0) and
                        (Users[i][13] == 'WAT_ROM_1')):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                       Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP* WaitN_fact
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = "WAIT_NO_URGENT"   
                        # print(WAIT_NU_INTRV)
                        # print(Sucep_Area[SUS])
            
            #------------    NEAR FIELD  WAI_N ROOM 1  CLOSE ------------------
            
            #               SETTING FOR  WAT_ROM_2 
            #  --------  FAR FIELD  WAI_N ROOM 2  INIT  --------
            cont_tot = 0
            cont_inf = 0
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and 
                    (Users[i][2] =='WAIT_NO_URGENT') and 
                    (Users[i][13] =='WAT_ROM_2') ):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
            infected = cont_inf 
            
            if infected > 0:
                # A1 = Tr_Pr['3_Wait_NoN'].loc[:,'m']
                A1 = Tr_Pr['10_WAIT_INTRV'].loc[:,'m']
                
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                # TP = Tr_Pr['3_Wait_NoN'].loc[index, infected]*TP_pyth
                TP = Tr_Pr['10_WAIT_INTRV'].loc[index, infected]*(TP_pyth*
                                                            Wait_intrv_fact)

                TP = TP * WaitN_fact
                Trnasmiss = random.random() < TP     
                # if Trnasmiss and (agent[1] == 0):
                if (Trnasmiss and (agent[1] == 0) and  
                    (agent[13] =='WAT_ROM_2')):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = "WAIT_NO_URGENT"
                    # print(WAIT_NU_INTRV)
                
            
            #------------    NEAR FIELD  WAI_N ROOM 2  INIT  -----------------
            Sucep_Area = []
            if agent[1] == 1:
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='WAIT_NO_URGENT') and
                       (Users[i][1] == 0) and
                        (Users[i][13] == 'WAT_ROM_2')):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                            Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP* WaitN_fact
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = "WAIT_NO_URGENT"   
                        # print(WAIT_NU_INTRV)
                        # print(Sucep_Area[SUS])
            
            #------------    NEAR FIELD  WAI_N ROOM 2  CLOSE ----------------
        
        else:
            cont_tot = 0
            cont_inf = 0
    
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and
                    (Users[i][2] =='WAIT_NO_URGENT')):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
            infected = cont_inf 
            
            if infected > 0:
                A1 = Tr_Pr['3_Wait_NoN'].loc[:,'m']
                # A1 = Tr_Pr['10_WAIT_INTRV'].loc[:,'m']
                
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['3_Wait_NoN'].loc[index, infected]*TP_pyth
                
                TP = TP*HEAD_wait_NU
                TP = TP * WaitN_fact
                # TP = TP*300
            
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = "WAIT_NO_URGENT"
                
                for i in range(len(Users)):
                    if( (Users[i][5] < currt_time) and 
                       (Users[i][2] =='WAIT_NO_URGENT') and
                        (Users[i] != agent) and
                        (Users[i][1] == 0) ):
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss and (agent[1] == 1):
                            Users[i][1] = 2
                            Users[i][9] = Curr_Area
                            Users[i][10] = day_current + 1 
                            Users[i][11] = "WAIT_NO_URGENT"
            
            
            #------------    NEAR FIELD  WAI_N  INIT  ---------------------
            
            Sucep_Area = []
            if agent[1] == 1:
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='WAIT_NO_URGENT') and
                       (Users[i][1] == 0)):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP* WaitN_fact
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = "WAIT_NO_URGENT"   
                        # print(Sucep_Area[SUS])
            
            #------------    NEAR FIELD  WAI_N  CLOSE ---------------------
            

    if AT_UR == Curr_Area:
# -------------------------- TRANSMIS PROBABILITY TOP -------------------------
# FAR - FIELD
# Here, we look for the total of infected in the room (PAT, NUR or DR), and 
# on that total, we take the FF TP and apply for any suscpt (PAT, NUR or DR)
#   1- Check if any infect in the room, PAT, NUR, DR, besides the entering one
#   2- if infected in the room - FF interaction time, the area time (agent[3])
#   3- FOR PAT
#       -TP for the area time, its applied with (who?) in area - HCW or PAT
#   4- FOR NURSE
#       -TP for the area time, its applied with (who?) in area - HCW or PAT
#   5- FOR DR
#       -TP for the area time, its applied with (who?) in area - HCW or PAT
#   6- If necesary, sends to additional test - LAB or IMAG
#       - calls function (time, agent, curr time)     
#
# NEAR-FIELD
#   Infected PAT
#   1- Search for suscp PAT (random selected) - estimate interaction time for 
#    NF TP
#       - if TP TRUE, suscep starts infect status
#   2- Search for NUR (rand select) - interact time NF proportion
#       - if TP TRUE, suscep starts infect status for NUR
#   3- Search for DR (rand select) - interact time NF proportion
#       - if TP TRUE, suscep starts infect status for DR
#
#  Infected HCW
#   1- search for a NUR and DR (rand)
#   2- if NUR or DR infcted - interact time NF proportion (NUR or DR time)
#   3- NF TP for proport of time - if TP TRUE
#       - if TP TRUE, suscep starts infect status for PAT
#  
# -------------------------- TRANSMIS PROBABILITY BOTTOM-----------------------


        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            cont_tot = 0
            cont_inf = 0
            cont_inf_2 = 0
            PAT_1 = 0
            PAT_2 = 0
            infected = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and 
                    (Users[i][2] =='ATTEN_URGE')
                    and (Users[i][15] != UNDEF ) ):
                    if ((Users[i][1] == 1) and 
                        (Users[i][15] == 'BEDS_1') or 
                        (Users[i][15] == 'BEDS_2') or 
                        (Users[i][15] == 'BEDS_3') ):
                        cont_inf = cont_inf + 1
                    if ((Users[i][1] == 1) and 
                        (Users[i][15] == 'BEDS_4') or 
                        (Users[i][15] == 'BEDS_5') or 
                        (Users[i][15] == 'BEDS_6') ):
                        cont_inf_2 = cont_inf_2 + 1

            PAT_1 = cont_inf
            PAT_2 = cont_inf_2


 
            for i in range(nur_NU_N_s1):
                if V_nurse_No_Urg_1[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
            for i in range(Dr_NU_s1):
                if dr_No_Urg_V_1[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = (cont_inf + cont_inf_2) + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                if infected > 5:
                    infected = 5
                TP = Tr_Pr['6_Atte_Urg_1'].loc[index, 
                                               infected]*TP_pyth
                TP = TP * Att_U_fact * HEAD_Att_U
                TP = TP*Att_interv
                for i in range(nur_NU_N_s1):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 
                                       or cont_inf_HCW != 0)):
                        if (V_nurse_No_Urg_1[i][1] == 0 and 
                            V_nurse_No_Urg_1[i][6] == 0):
                            V_nurse_No_Urg_1[i][3] = day_current + 1 
                            V_nurse_No_Urg_1[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                V_nurse_No_Urg_1[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                V_nurse_No_Urg_1[i][5] = 'Staff1_ATTEN_URGE'
                

                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff1_ATTEN_URGE"
                    if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                        agent[11] = PATIEN +'_ATTEN_URGE'
                    if cont_inf_HCW > (cont_inf + cont_inf_2):
                        agent[11] = 'Staff1_ATTEN_URGE'
                            
                
                for i in range(Dr_NU_s1):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 
                                       or cont_inf_HCW != 0)):
                        if (dr_No_Urg_V_1[i][1] == 0 and 
                            dr_No_Urg_V_1[i][6] == 0):
                            dr_No_Urg_V_1[i][3] = day_current + 1 
                            # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                            dr_No_Urg_V_1[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                dr_No_Urg_V_1[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                dr_No_Urg_V_1[i][5] = 'Staff1_ATTEN_URGE'
                
                med_test = random.random() < Medic_test
                if med_test:
                    med_test_funct_shift_1(agent,i, da, currt_time)

            #------------    NEAR FIELD  ATTEN_URGE  INIT  --------------------
          
            Sucep_Area = []
            # ------- Infected PAT, PAT - PAT Interact
            if agent[1] == 1:
                Inf_room = Area_1_U + Area_2_U
                if agent[15] in (Area_1_U):
                    Inf_room = Area_1_U
                elif agent[15] in (Area_2_U):
                    Inf_room = Area_2_U
                
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='ATTEN_URGE') and
                       (Users[i][1] == 0) and
                       (Users[i][15] in Inf_room )):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )

                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                      Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = PATIEN +'_ATTEN_URGE' 
                        # print(Sucep_Area[SUS])

                #              Patient-HCW_Nurse
                if len(V_nurse_No_Urg_1) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )

                if (V_nurse_No_Urg_1[SUS][1] == 0 and
                    V_nurse_No_Urg_1[SUS][6] == 0):
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_nurse_No_Urg_1[SUS][3] = day_current + 1
                        V_nurse_No_Urg_1[SUS][5] = PATIEN+'_ATTEN_URGE'
                        V_nurse_No_Urg_1[SUS][6] = day_current + 1 
                
                #              Patient-HCW_MD
                if len(dr_No_Urg_V_1) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(dr_No_Urg_V_1))-1 )

                if dr_No_Urg_V_1[SUS][1] == 0 and dr_No_Urg_V_1[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        dr_No_Urg_V_1[SUS][3] = day_current + 1
                        dr_No_Urg_V_1[SUS][5] = PATIEN+'_ATTEN_URGE'
                        dr_No_Urg_V_1[SUS][6] = day_current + 1             

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
            HCW_D = random.randint(0, (len(dr_No_Urg_V_1))-1 )
            # Infected Nurse
            if V_nurse_No_Urg_1[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff1_ATTEN_URGE'
            # Infected Medical doc
            if dr_No_Urg_V_1[HCW_D][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_M))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff1_ATTEN_URGE'     
               # -------------------------------------------------------------

            #------------    NEAR FIELD  ATTEN_URGE  CLOSE -------------------
        
    
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            cont_tot = 0
            cont_inf = 0
            cont_inf_2 = 0
            PAT_1 = 0
            PAT_2 = 0
            infected = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and 
                    (Users[i][2] =='ATTEN_URGE')
                    and (Users[i][15] != UNDEF ) ):
                    if ((Users[i][1] == 1) and 
                        (Users[i][15] == 'BEDS_1') or 
                        (Users[i][15] == 'BEDS_2') or 
                        (Users[i][15] == 'BEDS_3') ):
                        cont_inf = cont_inf + 1
                    if ((Users[i][1] == 1) and 
                        (Users[i][15] == 'BEDS_4') or 
                        (Users[i][15] == 'BEDS_5') or 
                        (Users[i][15] == 'BEDS_6') ):
                        cont_inf_2 = cont_inf_2 + 1

            PAT_1 = cont_inf
            PAT_2 = cont_inf_2
 
            for i in range(nur_NU_N_s2):
                if V_nurse_No_Urg_2[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
            for i in range(Dr_NU_s2):
                if dr_No_Urg_V_2[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = (cont_inf + cont_inf_2) + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                if infected > 5:
                    infected = 5
                TP = Tr_Pr['6_Atte_Urg_1'].loc[index, infected]*TP_pyth
                TP = TP * Att_U_fact * HEAD_Att_U
                TP = TP*Att_interv
                for i in range(nur_NU_N_s2):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 
                                       or cont_inf_HCW != 0)):
                        if (V_nurse_No_Urg_2[i][1] == 0 and 
                            V_nurse_No_Urg_2[i][6] == 0):
                            V_nurse_No_Urg_2[i][3] = day_current + 1 
                            V_nurse_No_Urg_2[i][5] = PATIEN+'_ATTEN_URGE'
                            V_nurse_No_Urg_2[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                V_nurse_No_Urg_2[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                V_nurse_No_Urg_2[i][5] = 'Staff2_ATTEN_URGE'
                

                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff2_ATTEN_URGE"
                    if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                        agent[11] = PATIEN +'_ATTEN_URGE'
                    if cont_inf_HCW > (cont_inf + cont_inf_2):
                        agent[11] = 'Staff2_ATTEN_URGE'
                            
                
                for i in range(Dr_NU_s2):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or
                                       cont_inf_HCW != 0)):
                        if (dr_No_Urg_V_2[i][1] == 0 and 
                            dr_No_Urg_V_2[i][6] == 0):
                            dr_No_Urg_V_2[i][3] = day_current + 1 
                            dr_No_Urg_V_2[i][5] = PATIEN+'_ATTEN_URGE'
                            dr_No_Urg_V_2[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                dr_No_Urg_V_2[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                dr_No_Urg_V_2[i][5] = 'Staff2_ATTEN_URGE'
                
                med_test = random.random() < Medic_test
                if med_test:
                    med_test_funct_shift_1(agent,i, da, currt_time)    

            #------------    NEAR FIELD  ATTEN_URGE  INIT  --------------------
            
            Sucep_Area = []
            if agent[1] == 1:
                
                Inf_room = Area_1_U + Area_2_U
                if agent[15] in (Area_1_U):
                    Inf_room = Area_1_U
                elif agent[15] in (Area_2_U):
                    Inf_room = Area_2_U
                
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='ATTEN_URGE') and
                       (Users[i][1] == 0) and
                       (Users[i][15] in Inf_room )):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = PATIEN +'_ATTEN_URGE' 
                        # print(Sucep_Area[SUS])

                #              Patient-HCW_Nurse
                if len(V_nurse_No_Urg_2) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(V_nurse_No_Urg_2))-1 )

                if (V_nurse_No_Urg_2[SUS][1] == 0 and 
                    V_nurse_No_Urg_2[SUS][6] == 0):
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_nurse_No_Urg_2[SUS][3] = day_current + 1
                        V_nurse_No_Urg_2[SUS][5] = PATIEN+'_ATTEN_URGE'
                        V_nurse_No_Urg_2[SUS][6] = day_current + 1 
                
                #              Patient-HCW_MD
                if len(dr_No_Urg_V_2) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(dr_No_Urg_V_2))-1 )

                if dr_No_Urg_V_2[SUS][1] == 0 and dr_No_Urg_V_2[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        dr_No_Urg_V_2[SUS][3] = day_current + 1
                        dr_No_Urg_V_2[SUS][5] = PATIEN+'_ATTEN_URGE'
                        dr_No_Urg_V_2[SUS][6] = day_current + 1 

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
            HCW_D = random.randint(0, (len(dr_No_Urg_V_2))-1 )
            # Infected Nurse
            if V_nurse_No_Urg_2[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                TP = Tr_Pr_NEAR['Near'].loc[index, 
                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff2_ATTEN_URGE'
            # Infected Medical doc
            if dr_No_Urg_V_2[HCW_D][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_M))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff2_ATTEN_URGE'     
            # -------------------------------------------------------------  



            #------------    NEAR FIELD  ATTEN_URGE  CLOSE --------------------
            
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
            
            cont_tot = 0
            cont_inf = 0
            cont_inf_2 = 0
            PAT_1 = 0
            PAT_2 = 0
            infected = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and 
                    (Users[i][2] =='ATTEN_URGE')
                    and (Users[i][15] != UNDEF ) ):
                    if ((Users[i][1] == 1) and 
                        (Users[i][15] == 'BEDS_1') or 
                        (Users[i][15] == 'BEDS_2') or 
                        (Users[i][15] == 'BEDS_3') ):
                        cont_inf = cont_inf + 1
                    if ((Users[i][1] == 1) and 
                        (Users[i][15] == 'BEDS_4') or 
                        (Users[i][15] == 'BEDS_5') or 
                        (Users[i][15] == 'BEDS_6') ):
                        cont_inf_2 = cont_inf_2 + 1

            PAT_1 = cont_inf
            PAT_2 = cont_inf_2
 
            for i in range(nur_NU_N_s3):
                if V_nurse_No_Urg_3[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
            for i in range(Dr_NU_s3):
                if dr_No_Urg_V_3[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = (cont_inf + cont_inf_2) + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                if infected > 5:
                    infected = 5
                TP = Tr_Pr['6_Atte_Urg_1'].loc[index, infected]*TP_pyth
                TP = TP * Att_U_fact * HEAD_Att_U
                TP = TP*Att_interv
                for i in range(nur_NU_N_s3):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 
                                       or cont_inf_HCW != 0)):
                        if (V_nurse_No_Urg_3[i][1] == 0 and 
                            V_nurse_No_Urg_3[i][6] == 0):
                            V_nurse_No_Urg_3[i][3] = day_current + 1 
                            V_nurse_No_Urg_3[i][5] = PATIEN+'_ATTEN_URGE'
                            V_nurse_No_Urg_3[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                V_nurse_No_Urg_3[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                V_nurse_No_Urg_3[i][5] = 'Staff3_ATTEN_URGE'
                

                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff3_ATTEN_URGE"
                    if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                        agent[11] = PATIEN +'_ATTEN_URGE'
                    elif cont_inf_HCW > (cont_inf + cont_inf_2):
                        agent[11] = 'Staff3_ATTEN_URGE'
                
                for i in range(Dr_NU_s3):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or 
                                       cont_inf_HCW != 0)):
                        if (dr_No_Urg_V_3[i][1] == 0 and 
                            dr_No_Urg_V_3[i][6] == 0):
                            dr_No_Urg_V_3[i][3] = day_current + 1 
                            dr_No_Urg_V_3[i][5] = PATIEN+'_ATTEN_URGE'
                            dr_No_Urg_V_3[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                dr_No_Urg_V_3[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                dr_No_Urg_V_3[i][5] = 'Staff3_ATTEN_URGE'
                
                med_test = random.random() < Medic_test
                if med_test:
                    med_test_funct_shift_1(agent,i, da, currt_time)

            #------------    NEAR FIELD  ATTEN_URGE  INIT  --------------------
            
            Sucep_Area = []
            if agent[1] == 1:
                
                Inf_room = Area_1_U + Area_2_U
                if agent[15] in (Area_1_U):
                    Inf_room = Area_1_U
                elif agent[15] in (Area_2_U):
                    Inf_room = Area_2_U
                
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='ATTEN_URGE') and
                       (Users[i][1] == 0) and
                       (Users[i][15] in Inf_room )):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = PATIEN +'_ATTEN_URGE' 
                        # print(Sucep_Area[SUS])

                #              Patient-HCW_Nurse
                if len(V_nurse_No_Urg_3) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(V_nurse_No_Urg_3))-1 )

                if (V_nurse_No_Urg_3[SUS][1] == 0 and 
                    V_nurse_No_Urg_3[SUS][6] == 0):
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_nurse_No_Urg_3[SUS][3] = day_current + 1
                        V_nurse_No_Urg_3[SUS][5] = PATIEN+'_ATTEN_URGE'
                        V_nurse_No_Urg_3[SUS][6] = day_current + 1 
                
                #              Patient-HCW_MD
                if len(dr_No_Urg_V_3) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(dr_No_Urg_V_3))-1 )

                if dr_No_Urg_V_3[SUS][1] == 0 and dr_No_Urg_V_3[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        dr_No_Urg_V_3[SUS][3] = day_current + 1
                        dr_No_Urg_V_3[SUS][5] = PATIEN+'_ATTEN_URGE'
                        dr_No_Urg_V_3[SUS][6] = day_current + 1             

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
            HCW_D = random.randint(0, (len(dr_No_Urg_V_3))-1 )
            # Infected Nurse
            if V_nurse_No_Urg_3[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff3_ATTEN_URGE'
            # Infected Medical doc
            if dr_No_Urg_V_3[HCW_D][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_M))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff3_ATTEN_URGE'     
            # ------------------------------------------------------------- 

            #------------    NEAR FIELD  ATTEN_URGE  CLOSE --------------------
                
    if At_NU == Curr_Area:  


        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            if ATTEN_NU_INTRV or CURTAINS_INTRV:    
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):

                    if ((Users[i][5] < currt_time) and 
                        (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2

                for i in range(nur_NU_N_s1):
                    if V_nurse_No_Urg_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s1):
                    if dr_No_Urg_V_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    # A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                        
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*(
                            TP_pyth*CURTAINS)
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*(
                            TP_pyth)

                    TP = TP * Att_N_fact
                    TP = TP*Att_interv
                    # TP = TP*0.5
                    TP = TP*Att_NU_pro
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(nur_NU_N_s1):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 
                                               or cont_inf_HCW != 0)):
                                if (V_nurse_No_Urg_1[i][1] == 0 and 
                                    V_nurse_No_Urg_1[i][6] == 0):
            
                                    V_nurse_No_Urg_1[i][3] = day_current + 1 
                                    V_nurse_No_Urg_1[i][5] ='Staff1_ATTE_N_URG'
                                    V_nurse_No_Urg_1[i][6] = day_current + 1 


                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(Dr_NU_s1):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or
                                               cont_inf_HCW != 0)):
                                if (dr_No_Urg_V_1[i][1] == 0 and 
                                    dr_No_Urg_V_1[i][6] == 0):
                                    dr_No_Urg_V_1[i][3] = day_current + 1 
                                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTE_N_URG'
                                    dr_No_Urg_V_1[i][6] = day_current + 1 

                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
            
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                #              Patient-Patient
                Sucep_Area = []
                if agent[1] == 1:
                    
                    
                    Curr_room = agent[15]
                    SUS = 0
                    for i in range(nur_NU_N_s1):
                        if (Curr_room == V_nurse_No_Urg_1[i][16] or 
                            Curr_room == V_nurse_No_Urg_1[i][18]) :
                            SUS = i
                    
                    HCW_N = SUS
                    HCW_D = SUS
                    
                    
                    #  Check in which room is the patient
                    #  Select the Nurse or MD attending that room
    
                    if (V_nurse_No_Urg_1[SUS][1] == 0 and
                        V_nurse_No_Urg_1[SUS][6] == 0):
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_1[SUS][3] = day_current + 1
                            V_nurse_No_Urg_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_1[SUS][6] = day_current + 1 
    
                    #              Patient-HCW_MD
    
                    if (dr_No_Urg_V_1[SUS][1] == 0 and 
                        dr_No_Urg_V_1[SUS][6] == 0):
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                      Mask[random.randint(0, 1)]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_1[SUS][3] = day_current + 1
                            dr_No_Urg_V_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_1[SUS][6] = day_current + 1 
    
                #   ----------       HCW infected - patient   -----------------
                #  Check in which room is the patient
                #  Select the Nurse or MD attending that room
                #  if the nurse or MD is infected, perform TP 
                
                Curr_room = agent[15]
                    
                SUS = 0
                for i in range(nur_NU_N_s1):
                    if (Curr_room == V_nurse_No_Urg_1[i][16] or 
                        Curr_room == V_nurse_No_Urg_1[i][18]) :
                        SUS = i
                # HCW_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
                # HCW_D = random.randint(0, (len(dr_No_Urg_V_1))-1 )
                HCW_N = SUS
                HCW_D = SUS
                # Infected Nurse
                if V_nurse_No_Urg_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_1[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'     
                    # --------------------------------------------------------
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
            
            else:
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    if ((Users[i][5] < currt_time) and 
                        (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2

                for i in range(nur_NU_N_s1):
                    if V_nurse_No_Urg_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s1):
                    if dr_No_Urg_V_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    TP = TP * Att_N_fact*HEAD_Att_NU
                    TP = TP*Att_interv
                    # TP = TP*0.5
                    TP = TP*Att_NU_pro
                    for i in range(nur_NU_N_s1):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or
                                           cont_inf_HCW != 0)):
                            if (V_nurse_No_Urg_1[i][1] == 0 and 
                                V_nurse_No_Urg_1[i][6] == 0):
       
                                V_nurse_No_Urg_1[i][3] = day_current + 1 
                                V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTE_N_URG'
                                V_nurse_No_Urg_1[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    V_nurse_No_Urg_1[i][5] = PATIEN +'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    V_nurse_No_Urg_1[i][5] = 'Staff1_ATTE_N_URG'
                                
                    

                    Trnasmiss = random.random() < TP     

                    if (Trnasmiss and (agent[1] == 0) ):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff1_ATTE_N_URG"
                        if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                            agent[11] = PATIEN +'_ATTE_N_URG'
                        elif cont_inf_HCW > (cont_inf + cont_inf_2):
                            agent[11] = 'Staff1_ATTE_N_URG'
                    
                    for i in range(Dr_NU_s1):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 
                                           or cont_inf_HCW != 0)):
                            if (dr_No_Urg_V_1[i][1] == 0 and 
                                dr_No_Urg_V_1[i][6] == 0):
       
                                dr_No_Urg_V_1[i][3] = day_current + 1 
                                dr_No_Urg_V_1[i][5] = PATIEN+'_ATTE_N_URG'
                                dr_No_Urg_V_1[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    dr_No_Urg_V_1[i][5] = PATIEN+'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
            
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                #              Patient-Patient
                Sucep_Area = []
                
                if agent[1] == 1:
                    Inf_room = Area_1 + Area_2
                    if agent[15] in (Area_1):
                        Inf_room = Area_1
                    elif agent[15] in (Area_2):
                        Inf_room = Area_2
                    
                    for i in range(len(Users)):
                        if((Users[i][5] < currt_time) and 
                           (Users[i][2] =='ATTE_N_URG') and
                           (Users[i][1] == 0) and
                           (Users[i][15] in Inf_room )):
                            Sucep_Area.append(Users[i])
                    if len(Sucep_Area) != 0:
                        if len(Sucep_Area) == 1:
                            SUS = 0
                        else:
                            SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            Sucep_Area[SUS][1] = 2
                            Sucep_Area[SUS][9] = Curr_Area
                            Sucep_Area[SUS][10] = day_current + 1 
                            Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                            # print(Sucep_Area[SUS])
                    
                    #              Patient-HCW_Nurse
                    
                    if len(V_nurse_No_Urg_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
    
                    if (V_nurse_No_Urg_1[SUS][1] == 0 and 
                        V_nurse_No_Urg_1[SUS][6] == 0):
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_1[SUS][3] = day_current + 1
                            V_nurse_No_Urg_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_1[SUS][6] = day_current + 1 
    
                    #              Patient-HCW_MD
                    if len(dr_No_Urg_V_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(dr_No_Urg_V_1))-1 )
    
                    if dr_No_Urg_V_1[SUS][1] == 0 and dr_No_Urg_V_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_1[SUS][3] = day_current + 1
                            dr_No_Urg_V_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_1[SUS][6] = day_current + 1 
    
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
                HCW_D = random.randint(0, (len(dr_No_Urg_V_1))-1 )
                # Infected Nurse
                if V_nurse_No_Urg_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_1[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'     
                   # ----------------------------------------------------------   
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
                

        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            if ATTEN_NU_INTRV or CURTAINS_INTRV:
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):

                    if ((Users[i][5] < currt_time) and
                        (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s2):
                    if V_nurse_No_Urg_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s2):
                    if dr_No_Urg_V_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    # A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    # TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth*CURTAINS
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth
                    
                    # TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth
                    TP = TP * Att_N_fact
                    TP = TP*Att_interv
                    # TP = TP*0.5
                    TP = TP*Att_NU_pro
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(nur_NU_N_s2):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 
                                               or cont_inf_HCW != 0)):
                                if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    V_nurse_No_Urg_2[i][3] = day_current + 1 
                                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTE_N_URG'
                                    V_nurse_No_Urg_2[i][6] = day_current + 1 
                               
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(Dr_NU_s2):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    dr_No_Urg_V_2[i][3] = day_current + 1 
                                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG'
                                    dr_No_Urg_V_2[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     dr_No_Urg_V_2[i][5] = PATIEN+'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                   
                    Curr_room = agent[15]
                    SUS = 0
                    for i in range(nur_NU_N_s2):
                        if (Curr_room == V_nurse_No_Urg_2[i][16] or 
                            Curr_room == V_nurse_No_Urg_2[i][18]) :
                            SUS = i
                    
                    HCW_N = SUS
                    HCW_D = SUS
                        
                    if V_nurse_No_Urg_2[SUS][1] == 0 and V_nurse_No_Urg_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_2[SUS][3] = day_current + 1
                            V_nurse_No_Urg_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_2[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    # if len(dr_No_Urg_V_2) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(dr_No_Urg_V_2))-1 )
    
                    if dr_No_Urg_V_2[SUS][1] == 0 and dr_No_Urg_V_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_2[SUS][3] = day_current + 1
                            dr_No_Urg_V_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_2[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                
                Curr_room = agent[15]
                # SUS = ROMS_G_NAM.index(Curr_room)
                
                SUS = 0
                for i in range(nur_NU_N_s2):
                    if (Curr_room == V_nurse_No_Urg_2[i][16] or 
                        Curr_room == V_nurse_No_Urg_2[i][18]) :
                        SUS = i
                
                # if Curr_room == 'ROOM_1':
                #     SUS = 0
                # elif Curr_room == 'ROOM_2':
                #     SUS = 1
                # elif Curr_room == 'ROOM_3':
                #     SUS = 2
                # # elif Curr_room == 'ROOM_4':
                # else:
                #     SUS = 3
                # HCW_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
                # HCW_D = random.randint(0, (len(dr_No_Urg_V_2))-1 )
                HCW_N = SUS
                HCW_D = SUS
                # Infected Nurse
                if V_nurse_No_Urg_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_2[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'     
                # -------------------------------------------------------------            
    
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
            
            else:
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):

                    if ((Users[i][5] < currt_time) and 
                        (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s2):
                    if V_nurse_No_Urg_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s2):
                    if dr_No_Urg_V_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    TP = TP * Att_N_fact * HEAD_Att_NU
                    TP = TP*Att_interv
                    # TP = TP*0.5
                    TP = TP*Att_NU_pro
                    for i in range(nur_NU_N_s2):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_nurse_No_Urg_2[i][3] = day_current + 1 
                                V_nurse_No_Urg_2[i][5] = PATIEN+'_ATTE_N_URG'
                                V_nurse_No_Urg_2[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    V_nurse_No_Urg_2[i][5] = PATIEN +'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTE_N_URG'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff2_ATTE_N_URG"
                        if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                            agent[11] = PATIEN +'_ATTE_N_URG'
                        if cont_inf_HCW >= (cont_inf + cont_inf_2):
                            agent[11] = 'Staff2_ATTE_N_URG'
                    
                    for i in range(Dr_NU_s2):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                dr_No_Urg_V_2[i][3] = day_current + 1 
                                dr_No_Urg_V_2[i][5] = PATIEN+'_ATTE_N_URG'
                                dr_No_Urg_V_2[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    dr_No_Urg_V_2[i][5] = PATIEN+'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                    Inf_room = Area_1 + Area_2
                    if agent[15] in (Area_1):
                        Inf_room = Area_1
                    elif agent[15] in (Area_2):
                        Inf_room = Area_2
                        
                    for i in range(len(Users)):
                        if((Users[i][5] < currt_time) and 
                           (Users[i][2] =='ATTE_N_URG') and
                           (Users[i][1] == 0) and
                           (Users[i][15] in Inf_room )):
                            Sucep_Area.append(Users[i])
                    if len(Sucep_Area) != 0:
                        if len(Sucep_Area) == 1:
                            SUS = 0
                        else:
                            SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            Sucep_Area[SUS][1] = 2
                            Sucep_Area[SUS][9] = Curr_Area
                            Sucep_Area[SUS][10] = day_current + 1 
                            Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                            # print(Sucep_Area[SUS])
                
                    #              Patient-HCW_Nurse
                    if len(V_nurse_No_Urg_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
    
                    if V_nurse_No_Urg_2[SUS][1] == 0 and V_nurse_No_Urg_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_2[SUS][3] = day_current + 1
                            V_nurse_No_Urg_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_2[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    if len(dr_No_Urg_V_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(dr_No_Urg_V_2))-1 )
    
                    if dr_No_Urg_V_2[SUS][1] == 0 and dr_No_Urg_V_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_2[SUS][3] = day_current + 1
                            dr_No_Urg_V_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_2[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
                HCW_D = random.randint(0, (len(dr_No_Urg_V_2))-1 )
                # Infected Nurse
                if V_nurse_No_Urg_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_2[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'     
                # -------------------------------------------------------------            
    
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------

        
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]): 
            
            if ATTEN_NU_INTRV or CURTAINS_INTRV:

                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s3):
                    if V_nurse_No_Urg_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s3):
                    if dr_No_Urg_V_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    
                    # A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                        
                    # TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth*CURTAINS
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth
                    
                    # TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth
                        
                    # TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth
                    TP = TP * Att_N_fact
                    TP = TP*Att_interv
                    # TP = TP*0.5
                    TP = TP*Att_NU_pro
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(nur_NU_N_s3):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    V_nurse_No_Urg_3[i][3] = day_current + 1 
                                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTE_N_URG'
                                    V_nurse_No_Urg_3[i][6] = day_current + 1 

                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(Dr_NU_s3):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    dr_No_Urg_V_3[i][3] = day_current + 1 
                                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG'
                                    dr_No_Urg_V_3[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     dr_No_Urg_V_3[i][5] = PATIEN+'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                    # for i in range(len(Users)):
                    #     if((Users[i][5] < currt_time) and 
                    #        (Users[i][2] =='ATTE_N_URG') and
                    #        (Users[i][1] == 0)):
                    #         Sucep_Area.append(Users[i])
                    # if len(Sucep_Area) != 0:
                    #     if len(Sucep_Area) == 1:
                    #         SUS = 0
                    #     else:
                    #         SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                    #     A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    #     # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    #     Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    #     diff = np.absolute(A1 - Share_time)
                    #     index = diff.argmin()
                    #     TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    #     Trnasmiss = random.random() < TP 
                    #     if Trnasmiss:
                    #         Sucep_Area[SUS][1] = 2
                    #         Sucep_Area[SUS][9] = Curr_Area
                    #         Sucep_Area[SUS][10] = day_current + 1 
                    #         Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                    #         # print(Sucep_Area[SUS])
                   
                  #                Patient-HCW_Nurse
                    # if len(V_nurse_No_Urg_3) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(V_nurse_No_Urg_3))-1 ) 
                    
                    Curr_room = agent[15]
                    SUS = 0
                    for i in range(nur_NU_N_s3):
                        if (Curr_room == V_nurse_No_Urg_3[i][16] or 
                            Curr_room == V_nurse_No_Urg_3[i][18]) :
                            SUS = i
                    
                    HCW_N = SUS
                    HCW_D = SUS
                    
                    
                    # Curr_room = agent[15]
                    
                    # if Curr_room == 'ROOM_1':
                    #     SUS = 0
                    # elif Curr_room == 'ROOM_2':
                    #     SUS = 1
                    # elif Curr_room == 'ROOM_3':
                    #     SUS = 2
                    # # elif Curr_room == 'ROOM_4':
                    # else:
                    #     SUS = 0
    
                    if V_nurse_No_Urg_3[SUS][1] == 0 and V_nurse_No_Urg_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_3[SUS][3] = day_current + 1
                            V_nurse_No_Urg_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_3[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    # if len(dr_No_Urg_V_3) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(dr_No_Urg_V_3))-1 )
    
                    if dr_No_Urg_V_3[SUS][1] == 0 and dr_No_Urg_V_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_3[SUS][3] = day_current + 1
                            dr_No_Urg_V_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_3[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                # HCW_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
                # HCW_D = random.randint(0, (len(dr_No_Urg_V_3))-1 )
                
                Curr_room = agent[15]
                # if Curr_room == 'ROOM_1':
                #     SUS = 0
                # elif Curr_room == 'ROOM_2':
                #     SUS = 1
                # elif Curr_room == 'ROOM_3':
                #     SUS = 2
                # # elif Curr_room == 'ROOM_4':
                # else:
                #     SUS = 0
                                
                SUS = 0
                for i in range(nur_NU_N_s3):
                    if (Curr_room == V_nurse_No_Urg_3[i][16] or 
                        Curr_room == V_nurse_No_Urg_3[i][18]) :
                        SUS = i
                    
                HCW_N = SUS
                HCW_D = SUS
                # Infected Nurse
                if V_nurse_No_Urg_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_3[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'     
                # ------------------------------------------------------------- 
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
            
            else:
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s3):
                    if V_nurse_No_Urg_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s3):
                    if dr_No_Urg_V_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    TP = TP * Att_N_fact * HEAD_Att_NU
                    TP = TP*Att_interv
                    # TP = TP*0.5
                    TP = TP*Att_NU_pro
                    for i in range(nur_NU_N_s3):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_nurse_No_Urg_3[i][3] = day_current + 1 
                                V_nurse_No_Urg_3[i][5] = PATIEN+'_ATTE_N_URG'
                                V_nurse_No_Urg_3[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    V_nurse_No_Urg_3[i][5] = PATIEN +'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTE_N_URG'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff3_ATTE_N_URG"
                        if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                            agent[11] = PATIEN +'_ATTE_N_URG'
                        if cont_inf_HCW > (cont_inf + cont_inf_2):
                            agent[11] = 'Staff3_ATTE_N_URG'
                    
                    for i in range(Dr_NU_s3):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                dr_No_Urg_V_3[i][3] = day_current + 1 
                                dr_No_Urg_V_3[i][5] = PATIEN+'_ATTE_N_URG'
                                dr_No_Urg_V_3[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    dr_No_Urg_V_3[i][5] = PATIEN+'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                    Inf_room = Area_1 + Area_2
                    if agent[15] in (Area_1):
                        Inf_room = Area_1
                    elif agent[15] in (Area_2):
                        Inf_room = Area_2
                        
                    for i in range(len(Users)):
                        if((Users[i][5] < currt_time) and 
                           (Users[i][2] =='ATTE_N_URG') and
                           (Users[i][1] == 0) and
                           (Users[i][15] in Inf_room )):
                            Sucep_Area.append(Users[i])
                    if len(Sucep_Area) != 0:
                        if len(Sucep_Area) == 1:
                            SUS = 0
                        else:
                            SUS = random.randint(0, (len(Sucep_Area))-1 )
                
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            Sucep_Area[SUS][1] = 2
                            Sucep_Area[SUS][9] = Curr_Area
                            Sucep_Area[SUS][10] = day_current + 1 
                            Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                            # print(Sucep_Area[SUS])
                   
                    #              Patient-HCW_Nurse
                    if len(V_nurse_No_Urg_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
    
                    if V_nurse_No_Urg_3[SUS][1] == 0 and V_nurse_No_Urg_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_3[SUS][3] = day_current + 1
                            V_nurse_No_Urg_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_3[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    if len(dr_No_Urg_V_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(dr_No_Urg_V_3))-1 )
    
                    if dr_No_Urg_V_3[SUS][1] == 0 and dr_No_Urg_V_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_3[SUS][3] = day_current + 1
                            dr_No_Urg_V_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_3[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
                HCW_D = random.randint(0, (len(dr_No_Urg_V_3))-1 )
                # Infected Nurse
                if V_nurse_No_Urg_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_3[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'     
                # ------------------------------------------------------------- 
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------

    return agent

     
"""----------------------------------------------------------------------------
                   ROUTINE MEDICAL TEST SHIFT 1
"""

def med_test_funct_shift_1(agent, i, day, currt_time):
    
    day_current = day
    Immagin = random.random() < 0.5
    t_med_test = random.randint(1, 60)
    agent[8] = agent[2]
    # Users[i][3] = t_med_test
    # agent[7] = agent[6] + t_med_test
    
    if Immagin:
        
        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(imagi_N):
                    if V_imagin_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                # Add counter to cont_inf_HCW (+1) if agent[1] == 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                    
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['7_Imaging'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['7_Imaging'].loc[index, infected]
                    # if TP > 100:
                    #     TP = TP*0.001
                    TP = TP * Imagi_fact * HEAD_Imag
                    TP = TP*TP_pyth
                    for i in range(imagi_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_imagin_1[i][1] == 0 and V_imagin_1[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_imagin_1[i][3] = day_current + 1 
                                # V_imagin_1[i][5] = PATIEN +'_IMAGING'
                                V_imagin_1[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_imagin_1[i][5] = PATIEN +'_IMAGING'
                                elif cont_inf_HCW != 0:
                                    V_imagin_1[i][5] = 'Staff1_IMAGING'
                                
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='IMAGING'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_IMAGING'
                               
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_imagin_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_imagin_1))-1 )
    
                    if V_imagin_1[SUS][1] == 0 and V_imagin_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_imagin_1[SUS][3] = day_current + 1
                            V_imagin_1[SUS][5] = PATIEN +'_IMAGING'
                            V_imagin_1[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_imagin_1))-1 )
                # Infected Nurse
                if V_imagin_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_IMAGING'
                # ------------------------------------------------------------- 
                
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(imagi_N):
                    if V_imagin_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1

                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['7_Imaging'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['7_Imaging'].loc[index, infected]
                    # if TP > 100:
                    #     TP = TP*0.001
                    TP = TP * Imagi_fact * HEAD_Imag
                    TP = TP*TP_pyth
                    for i in range(imagi_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_imagin_2[i][1] == 0 and V_imagin_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_imagin_2[i][3] = day_current + 1 
                                V_imagin_2[i][5] = PATIEN+'_IMAGING'
                                V_imagin_2[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_imagin_2[i][5] = PATIEN +'_IMAGING'
                                elif cont_inf_HCW != 0:
                                    V_imagin_2[i][5] = 'Staff2_IMAGING'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='IMAGING'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2_IMAGING"
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_imagin_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_imagin_2))-1 )
    
                    if V_imagin_2[SUS][1] == 0 and V_imagin_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_imagin_2[SUS][3] = day_current + 1
                            V_imagin_2[SUS][5] = PATIEN +'_IMAGING'
                            V_imagin_2[SUS][6] = day_current + 1 

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_imagin_2))-1 )
                # Infected Nurse
                if V_imagin_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_IMAGING'
                # ------------------------------------------------------------- 
    
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(imagi_N):
                    if V_imagin_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1

                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                    
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['7_Imaging'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['7_Imaging'].loc[index, infected]
                    # if TP > 100:
                    #     TP = TP*0.001
                    TP = TP * Imagi_fact * HEAD_Imag
                    TP = TP*TP_pyth
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_imagin_3[i][1] == 0 and V_imagin_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_imagin_3[i][3] = day_current + 1 
                                V_imagin_3[i][5] = PATIEN+'_IMAGING'
                                V_imagin_3[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_imagin_3[i][5] = PATIEN +'_IMAGING'
                                elif cont_inf_HCW != 0:
                                    V_imagin_3[i][5] = 'Staff3_IMAGING'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='IMAGING'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3_IMAGING"
                
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_imagin_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_imagin_3))-1 )
    
                    if V_imagin_3[SUS][1] == 0 and V_imagin_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_imagin_3[SUS][3] = day_current + 1
                            V_imagin_3[SUS][5] = PATIEN +'_IMAGING'
                            V_imagin_3[SUS][6] = day_current + 1 
    
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_imagin_3))-1 )
                # Infected Nurse
                if V_imagin_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_IMAGING'
                # ------------------------------------------------------------- 

    
    else:
        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(labor_N):
                    if V_labor_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['8_Laborat'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['8_Laborat'].loc[index, infected]
                    # if TP > 100:
                    #     TP = TP*0.001
                    TP = TP * Labor_fact * HEAD_Labor
                    TP = TP*TP_pyth
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_labor_1[i][1] == 0 and V_labor_1[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_labor_1[i][3] = day_current + 1 
                                V_labor_1[i][5] = PATIEN+'_LABORATORY'
                                V_labor_1[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_labor_1[i][5] = PATIEN +'_LABORATORY'
                                elif cont_inf_HCW != 0:
                                    V_labor_1[i][5] = 'Staff1_LABORATORY'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='LABORATORY'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1_LABORATORY"
    
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_labor_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_labor_1))-1 )
    
                    if V_labor_1[SUS][1] == 0 and V_labor_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_labor_1[SUS][3] = day_current + 1
                            V_labor_1[SUS][5] = PATIEN +'_LABORATORY'
                            V_labor_1[SUS][6] = day_current + 1 

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_labor_1))-1 )
                # Infected Nurse
                if V_labor_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_LABORATORY'
                # ------------------------------------------------------------- 
    
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(labor_N):
                    if V_labor_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['8_Laborat'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['8_Laborat'].loc[index, infected]
                    # if TP > 100:
                    #     TP = TP*0.001
                    TP = TP * Labor_fact * HEAD_Labor
                    TP = TP*TP_pyth
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_labor_2[i][1] == 0 and V_labor_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_labor_2[i][3] = day_current + 1 
                                V_labor_2[i][5] = PATIEN+'_LABORATORY'
                                V_labor_2[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_labor_2[i][5] = PATIEN +'_LABORATORY'
                                elif cont_inf_HCW != 0:
                                    V_labor_2[i][5] = 'Staff2_LABORATORY'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='LABORATORY'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2_LABORATORY"

                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_labor_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_labor_2))-1 )
    
                    if V_labor_2[SUS][1] == 0 and V_labor_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_labor_2[SUS][3] = day_current + 1
                            V_labor_2[SUS][5] = PATIEN +'_LABORATORY'
                            V_labor_2[SUS][6] = day_current + 1     

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_labor_2))-1 )
                # Infected Nurse
                if V_labor_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_LABORATORY'
                # ------------------------------------------------------------- 

        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(labor_N):
                    if V_labor_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1

                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['8_Laborat'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['8_Laborat'].loc[index, infected]
                    # if TP > 100:
                    #     TP = TP*0.001
                    TP = TP * Labor_fact * HEAD_Labor
                    TP = TP*TP_pyth
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_labor_3[i][1] == 0 and V_labor_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_labor_3[i][3] = day_current + 1 
                                V_labor_3[i][5] = PATIEN+'_LABORATORY'
                                V_labor_3[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_labor_3[i][5] = PATIEN +'_LABORATORY'
                                elif cont_inf_HCW != 0:
                                    V_labor_3[i][5] = 'Staff3_LABORATORY'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='LABORATORY'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3_LABORATORY"
                        
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_labor_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_labor_3))-1 )
    
                    if V_labor_3[SUS][1] == 0 and V_labor_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_labor_3[SUS][3] = day_current + 1
                            V_labor_3[SUS][5] = PATIEN +'_LABORATORY'
                            V_labor_3[SUS][6] = day_current + 1 

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_labor_3))-1 )
                # Infected Nurse
                if V_labor_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_LABORATORY'
                # ------------------------------------------------------------- 
        

    return


"""----------------------------------------------------------------------------
                          ROUTINE HCW SETTING 1
"""
def workers_settings(worker1, worker2, worker3):
        
        Users_workers_shift_1 = worker1
        Users_workers_shift_2 = worker2
        Users_workers_shift_3 = worker3
        
        
        for i in range(recep_N_s1):
            Users_workers_shift_1.append(V_recep_1[i])
        for i in range(recep_N_s2):
            Users_workers_shift_2.append(V_recep_2[i])
        for i in range(recep_N_s3):
            Users_workers_shift_3.append(V_recep_3[i])
    
        for i in range(triag_N_s1):
            Users_workers_shift_1.append(V_triag_1[i])
        for i in range(triag_N_s2):
            Users_workers_shift_2.append(V_triag_2[i])
        for i in range(triag_N_s3):
            Users_workers_shift_3.append(V_triag_3[i])
        
        for i in range(nur_NU_N_s1):
            Users_workers_shift_1.append(V_nurse_No_Urg_1[i])
        for i in range(nur_NU_N_s2):
            Users_workers_shift_2.append(V_nurse_No_Urg_2[i])
        for i in range(nur_NU_N_s3):
            Users_workers_shift_3.append(V_nurse_No_Urg_3[i])
        
        for i in range(Dr_NU_s1):
            Users_workers_shift_1.append(dr_No_Urg_V_1[i])
        for i in range(Dr_NU_s2):
            Users_workers_shift_2.append(dr_No_Urg_V_2[i])
        for i in range(Dr_NU_s3):    
            Users_workers_shift_3.append(dr_No_Urg_V_3[i])
        

        for i in range(imagi_N):
            Users_workers_shift_1.append(V_imagin_1[i])
            Users_workers_shift_2.append(V_imagin_2[i])
            Users_workers_shift_3.append(V_imagin_3[i])
        
        for i in range(labor_N):
            Users_workers_shift_1.append(V_labor_1[i])
            Users_workers_shift_2.append(V_labor_2[i])
            Users_workers_shift_3.append(V_labor_3[i])
    
    
        return Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3
 
"""----------------------------------------------------------------------------
                          ROUTINE HCW INFECTION STATUS
"""    
def workers_settings_status(worker1, worker2, worker3, days):
    day_current = days
    Users_workers_shift_1 = worker1
    Users_workers_shift_2 = worker2
    Users_workers_shift_3 = worker3
    
    # ------------------   shift 1    -----------------------------------------
    
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] != 0) and (Users_workers_shift_1[i][4] == 0):
            Users_workers_shift_1[i][4] = Users_workers_shift_1[i][3] + 3 #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_1[i][9] = 'Not_Infectious'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_1[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_1[i][11] = Users_workers_shift_1[i][3] + 5 #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_1[i][11] != 0)and (Users_workers_shift_1[i][10] == UNDEF): 
         #   Users_workers_shift_1[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] != 0) and (Users_workers_shift_1[i][4] != 0):
            Users_workers_shift_1[i][3] = day_current + 1 #reupdate index 3 to continue counter for the number of days
    
    for i in range(len(Users_workers_shift_1)):
        if ((Users_workers_shift_1[i][3] == Users_workers_shift_1[i][4]) and 
                                     (Users_workers_shift_1[i][5] != UNDEF )):
            Users_workers_shift_1[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][4]) and (Users_workers_shift_1[i][1] == 1) :
            Users_workers_shift_1[i][12] = Users_workers_shift_1[i][3] + 5 #infectious , can spread infections after 5 days
            Users_workers_shift_1[i][9] = 'infectious'
            
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][12])and (Users_workers_shift_1[i][9] == 'infectious') :
            #Users_workers_shift_1[i][13] = Users_workers_shift_1[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_1[i][14] = 'immune'
            

    for i in range(len(Users_workers_shift_1)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][11]) and  (Users_workers_shift_1[i][10] =='No symptom') and (Users_workers_shift_1[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_1[i][7] = SYMP_NO
            else:
                Users_workers_shift_1[i][7] = SYMP_YES            
    
                
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][7] == SYMP_YES) and (Users_workers_shift_1[i][9] == 'infectious') :
            if Users_workers_shift_1[i][8] == REPLACE:
                Users_workers_shift_1[i][13] = Users_workers_shift_1[i][13] + 1
            Users_workers_shift_1[i][8] = REPLACE
            Users_workers_shift_1[i][1] = 0
            Users_workers_shift_1[i][4] = 0
            Users_workers_shift_1[i][5] = UNDEF
            Users_workers_shift_1[i][6] = 0
            Users_workers_shift_1[i][7] = UNDEF
            Users_workers_shift_1[i][9] = UNDEF
            Users_workers_shift_1[i][10] = UNDEF
            Users_workers_shift_1[i][11] = 0
            Users_workers_shift_1[i][12] = 0
            #Users_workers_shift_1[i][13] = 0
            Users_workers_shift_1[i][14] = UNDEF
            
        if (Users_workers_shift_1[i][10] == 'No symptom')and (Users_workers_shift_1[i][14] == 'immune') : 
            Users_workers_shift_1[i][1] = 0 
            Users_workers_shift_1[i][9] = UNDEF
            
           
    # ------------------   shift 2    -----------------------------------------
            
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] != 0) and (Users_workers_shift_2[i][4] == 0):
            Users_workers_shift_2[i][4] = Users_workers_shift_2[i][3] + 3 #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_2[i][9] = 'Not_Infectious'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_2[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_2[i][11] = Users_workers_shift_2[i][3] + 5 #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_2[i][11] != 0)and (Users_workers_shift_2[i][10] == UNDEF): 
         #   Users_workers_shift_2[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] != 0) and (Users_workers_shift_2[i][4] != 0):
            Users_workers_shift_2[i][3] = day_current + 1#reupdate index 3 to continue counter for the number of days
     
    for i in range(len(Users_workers_shift_2)):
        if ((Users_workers_shift_2[i][3] == Users_workers_shift_2[i][4]) and 
                                     (Users_workers_shift_2[i][5] != UNDEF )):
            Users_workers_shift_2[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][4]) and (Users_workers_shift_2[i][1] == 1) :
            Users_workers_shift_2[i][12] = Users_workers_shift_2[i][3] + 5 #infectious , can spread infections after 5 days
            Users_workers_shift_2[i][9] = 'infectious'
            
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][12])and (Users_workers_shift_2[i][9] == 'infectious') :
            #Users_workers_shift_2[i][13] = Users_workers_shift_2[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_2[i][14] = 'immune'
            

    for i in range(len(Users_workers_shift_2)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][11]) and  (Users_workers_shift_2[i][10] =='No symptom') and (Users_workers_shift_2[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_2[i][7] = SYMP_NO
            else:
                Users_workers_shift_2[i][7] = SYMP_YES         
    

                
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][7] == SYMP_YES) and (Users_workers_shift_2[i][9] == 'infectious') :
            if Users_workers_shift_2[i][8] == REPLACE:
                Users_workers_shift_2[i][13] = Users_workers_shift_2[i][13] + 1
            Users_workers_shift_2[i][8] = REPLACE
            Users_workers_shift_2[i][1] = 0
            Users_workers_shift_2[i][4] = 0
            Users_workers_shift_2[i][5] = UNDEF
            Users_workers_shift_2[i][6] = 0
            Users_workers_shift_2[i][7] = UNDEF
            Users_workers_shift_2[i][9] = UNDEF
            Users_workers_shift_2[i][10] = UNDEF
            Users_workers_shift_2[i][11] = 0
            Users_workers_shift_2[i][12] = 0
            # Users_workers_shift_2[i][13] = 0
            Users_workers_shift_2[i][14] = UNDEF
            
            
        if (Users_workers_shift_2[i][10] == 'No symptom')and (Users_workers_shift_2[i][14] == 'immune') : 
            Users_workers_shift_2[i][1] = 0 
            Users_workers_shift_2[i][9] = UNDEF
            
        
    # ------------------   shift 3    -----------------------------------------
            
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] != 0) and (Users_workers_shift_3[i][4] == 0):
            Users_workers_shift_3[i][4] = Users_workers_shift_3[i][3] + 3 #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_3[i][9] = 'Not_Infectious'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_3[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_3[i][11] = Users_workers_shift_3[i][3] + 5 #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_3[i][11] != 0)and (Users_workers_shift_3[i][10] == UNDEF): 
         #   Users_workers_shift_3[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] != 0) and (Users_workers_shift_3[i][4] != 0):
            Users_workers_shift_3[i][3] = day_current + 1#reupdate index 3 to continue counter for the number of days
    
    for i in range(len(Users_workers_shift_3)):
        if ((Users_workers_shift_3[i][3] == Users_workers_shift_3[i][4]) and 
                                     (Users_workers_shift_3[i][5] != UNDEF )):
            Users_workers_shift_3[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][4]) and (Users_workers_shift_3[i][1] == 1) :
            Users_workers_shift_3[i][12] = Users_workers_shift_3[i][3] + 5 #infectious , can spread infections after 5 days
            Users_workers_shift_3[i][9] = 'infectious'
            
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][12])and (Users_workers_shift_3[i][9] == 'infectious') :
            #Users_workers_shift_3[i][13] = Users_workers_shift_3[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_3[i][14] = 'immune'
                      
        
    for i in range(len(Users_workers_shift_3)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][11]) and  (Users_workers_shift_3[i][10] =='No symptom') and (Users_workers_shift_3[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_3[i][7] = SYMP_NO
            else:
                Users_workers_shift_3[i][7] = SYMP_YES           
    
    
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][7] == SYMP_YES) and (Users_workers_shift_3[i][9] == 'infectious') :
            if Users_workers_shift_3[i][8] == REPLACE:
                Users_workers_shift_3[i][13] = Users_workers_shift_3[i][13] + 1
            Users_workers_shift_3[i][8] = REPLACE
            Users_workers_shift_3[i][1] = 0
            Users_workers_shift_3[i][4] = 0
            Users_workers_shift_3[i][5] = UNDEF
            Users_workers_shift_3[i][6] = 0
            Users_workers_shift_3[i][7] = UNDEF
            Users_workers_shift_3[i][9] = UNDEF
            Users_workers_shift_3[i][10] = UNDEF
            Users_workers_shift_3[i][11] = 0
            Users_workers_shift_3[i][12] = 0
            #Users_workers_shift_3[i][13] = 0
            Users_workers_shift_3[i][14] = UNDEF
            
                                                
        if (Users_workers_shift_3[i][10] == 'No symptom')and (Users_workers_shift_3[i][14] == 'immune') : 
            Users_workers_shift_3[i][1] = 0 
            Users_workers_shift_3[i][9] = UNDEF
    
    return Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3



def meet_HCW_1():
#---------------------------- TRANS PROB  INIT -----------------------------
# FAR -FIELD
# 1- Count the total of infected HCWs of the area
# 2- Check FF TP for time_area_HCW and appy for each HCW of the area  
#
# NEAR FIELD
# 1- Random select a HCW from area, account for the total of inf from FAR-FIELD
# 2- if suscept, apply NF TP for Prop_H_H_Recep
#
#---------------------------- TRANS PROB BOTOM -------------------------------

    
    #  -------  RECEPTION --------------------
    cont_inf_HCW = 0
    infe_WCH = 0
    for i in range(recep_N_s1):
        if V_recep_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH = V_recep_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Recep_fact
        for i in range(recep_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_recep_1[i][1] == 0 and V_recep_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_recep_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_recep_1[i][6] = day_current + 1 
                    V_recep_1[i][5] = 'Staff1_RECEPTION' 
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_recep_1))-1 )
    if ( (infe_WCH != 0) and  
            (V_recep_1[Sus_HCW][1] == 0 and V_recep_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Recep)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                            Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_recep_1[Sus_HCW][3] = day_current + 1
            V_recep_1[Sus_HCW][5] = 'Staff1_RECEPTION' 
            V_recep_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------   

    
    #  -------  TRIAGE --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(triag_N_s1):
        if V_triag_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_triag_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Triag_fact
        for i in range(triag_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_triag_1[i][1] == 0 and V_triag_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_triag_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_triag_1[i][6] = day_current + 1 
                    V_triag_1[i][5] = 'Staff1_TRIAGE'
    
        # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_triag_1))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_triag_1[Sus_HCW][1] == 0 and V_triag_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Triag)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_triag_1[Sus_HCW][3] = day_current + 1
            V_triag_1[Sus_HCW][5] = 'Staff1_TRIAGE' 
            V_triag_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------   
    
    #  -------  ATTEN_URGE --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s1):
        if V_nurse_No_Urg_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_1[i])
    for i in range(Dr_NU_s1):
        if dr_No_Urg_V_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_1[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        TP = Tr_Pr['6_Atte_Urg_1'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Att_U_fact * HEAD_Att_U
        for i in range(nur_NU_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_1[i][6] = day_current + 1 
                    V_nurse_No_Urg_1[i][5] = 'Staff1_ATTEN_URGE' 
        for i in range(Dr_NU_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_1[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_1[i][6] = day_current + 1 
                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTEN_URGE'    
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_1))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if ((random.random() < TP) and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTEN_URGE' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTEN_URGE' 
        if ((random.random() < TP) and (dr_No_Urg_V_1[Sus_M][1] == 0) and
            (dr_No_Urg_V_1[Sus_M][6] == 0) ):
            dr_No_Urg_V_1[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_1[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_1[Sus_M][5] = 'Staff1_ATTEN_URGE' 
    
    # -----------------  Near Field close   ------------------------
    
    #  -------  ATTE_N_URG --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s1):
        if V_nurse_No_Urg_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_1[i])
    for i in range(Dr_NU_s1):
        if dr_No_Urg_V_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_1[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        
        if CURTAINS_INTRV:
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth*CURTAINS
        # else: 
        #     TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
            TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, cont_inf_HCW]*TP_pyth
        else: 
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth

        TP = TP * Att_N_fact * HEAD_Att_NU
        # TP = TP*ATT_NU_H_H
        for i in range(nur_NU_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_1[i][6] = day_current + 1 
                    V_nurse_No_Urg_1[i][5] = 'Staff1_ATTE_N_URG' 
        for i in range(Dr_NU_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_1[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_1[i][6] = day_current + 1 
                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTE_N_URG' 
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_1))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index,
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if ((random.random() < TP) and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTE_N_URG' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTE_N_URG' 
        if ((random.random() < TP) and (dr_No_Urg_V_1[Sus_M][1] == 0) and
            (dr_No_Urg_V_1[Sus_M][6] == 0) ):
            dr_No_Urg_V_1[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_1[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_1[Sus_M][5] = 'Staff1_ATTE_N_URG' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  IMAGING --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(imagi_N):
        if V_imagin_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_imagin_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['7_Imaging'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['7_Imaging'].loc[index, cont_inf_HCW]
        # if TP > 100:
        #     TP = TP*0.001
        TP = TP * Imagi_fact * HEAD_Imag
        TP = TP*TP_pyth
        
        for i in range(imagi_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_imagin_1[i][1] == 0 and V_imagin_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_imagin_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_imagin_1[i][6] = day_current + 1 
                    V_imagin_1[i][5] = 'Staff1_IMAGING'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_imagin_1))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_imagin_1[Sus_HCW][1] == 0 and V_imagin_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_imagin_1[Sus_HCW][3] = day_current + 1
            V_imagin_1[Sus_HCW][5] = 'Staff1_IMAGING' 
            V_imagin_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  LABORATORY --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(labor_N):
        if V_labor_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_labor_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['8_Laborat'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['8_Laborat'].loc[index, cont_inf_HCW]
        # if TP > 100:
        #     TP = TP*0.001
        TP = TP*TP_pyth
        TP = TP * Labor_fact * HEAD_Labor
        
        for i in range(labor_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_labor_1[i][1] == 0 and V_labor_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_labor_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_labor_1[i][6] = day_current + 1 
                    V_labor_1[i][5] = 'Staff1_LABORATORY'

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_labor_1))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_labor_1[Sus_HCW][1] == 0 and V_labor_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index,
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_labor_1[Sus_HCW][3] = day_current + 1
            V_labor_1[Sus_HCW][5] = 'Staff1_LABORATORY' 
            V_labor_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 

    return



def meet_HCW_2():
    
#---------------------------- TRANS PROB  INIT --------------------------------
# FAR -FIELD
# 1- Count the total of infected HCWs of the area
# 2- Check FF TP for time_area_HCW and appy for each HCW of the area  
#
# NEAR FIELD
# 1- Random select a HCW from area, account for the total of inf from FAR-FIELD
# 2- if suscept, apply NF TP for Prop_H_H_Recep
#
#---------------------------- TRANS PROB BOTOM --------------------------------

    
    #  -------  RECEPTION --------------------
    cont_inf_HCW = 0
    infe_WCH = 0
    for i in range(recep_N_s2):
        if V_recep_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH = V_recep_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Recep_fact
        for i in range(recep_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_recep_2[i][1] == 0 and V_recep_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_recep_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_recep_2[i][6] = day_current + 1 
                    V_recep_2[i][5] = 'Staff2_RECEPTION' 

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_recep_2))-1 )
    if ( (infe_WCH != 0) and  
            (V_recep_2[Sus_HCW][1] == 0 and V_recep_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Recep)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_recep_2[Sus_HCW][3] = day_current + 1
            V_recep_2[Sus_HCW][5] = 'Staff2_RECEPTION' 
            V_recep_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------   
    
    
    #  -------  TRIAGE --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(triag_N_s2):
        if V_triag_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_triag_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Triag_fact
        for i in range(triag_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_triag_2[i][1] == 0 and V_triag_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_triag_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_triag_2[i][6] = day_current + 1 
                    V_triag_2[i][5] = 'Staff2_TRIAGE'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_triag_2))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_triag_2[Sus_HCW][1] == 0 and V_triag_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Triag)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index,
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_triag_2[Sus_HCW][3] = day_current + 1
            V_triag_2[Sus_HCW][5] = 'Staff2_TRIAGE' 
            V_triag_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  ATTEN_URGE --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s2):
        if V_nurse_No_Urg_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_2[i])
    for i in range(Dr_NU_s2):
        if dr_No_Urg_V_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_2[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        TP = Tr_Pr['6_Atte_Urg_1'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Att_U_fact * HEAD_Att_U
        for i in range(nur_NU_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_2[i][6] = day_current + 1 
                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTEN_URGE' 
        for i in range(Dr_NU_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_2[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_2[i][6] = day_current + 1 
                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTEN_URGE'    
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_2))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTEN_URGE' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTEN_URGE' 
        if ((random.random() < TP) and (dr_No_Urg_V_1[Sus_M][1] == 0) and
            (dr_No_Urg_V_2[Sus_M][6] == 0) ):
            dr_No_Urg_V_2[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_2[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_2[Sus_M][5] = 'Staff2_ATTEN_URGE' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  ATTE_N_URG --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s2):
        if V_nurse_No_Urg_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_2[i])
    for i in range(Dr_NU_s2):
        if dr_No_Urg_V_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_2[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        
        if CURTAINS_INTRV:
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth*CURTAINS
        # else: 
        #     TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
            TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, cont_inf_HCW]*TP_pyth
        else: 
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        
        # TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Att_N_fact * HEAD_Att_NU
        # TP = TP*ATT_NU_H_H
        for i in range(nur_NU_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_2[i][6] = day_current + 1 
                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTE_N_URG' 
        for i in range(Dr_NU_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_2[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_2[i][6] = day_current + 1 
                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG' 
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_2))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTE_N_URG' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTE_N_URG' 
        if ((random.random() < TP) and (dr_No_Urg_V_2[Sus_M][1] == 0) and
            (dr_No_Urg_V_2[Sus_M][6] == 0) ):
            dr_No_Urg_V_2[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_2[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_2[Sus_M][5] = 'Staff2_ATTE_N_URG' 
    
    # -----------------  Near Field close   ------------------------
    
    #  -------  IMAGING --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(imagi_N):
        if V_imagin_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_imagin_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['7_Imaging'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['7_Imaging'].loc[index, cont_inf_HCW]
        # if TP > 100:
        #     TP = TP*0.001
        TP = TP * Imagi_fact * HEAD_Imag
        TP = TP*TP_pyth
        
        for i in range(imagi_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_imagin_2[i][1] == 0 and V_imagin_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_imagin_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_imagin_2[i][6] = day_current + 1 
                    V_imagin_2[i][5] = 'Staff2_IMAGING'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_imagin_2))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_imagin_2[Sus_HCW][1] == 0 and V_imagin_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_imagin_2[Sus_HCW][3] = day_current + 1
            V_imagin_2[Sus_HCW][5] = 'Staff2_IMAGING' 
            V_imagin_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  LABORATORY --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(labor_N):
        if V_labor_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_labor_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['8_Laborat'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['8_Laborat'].loc[index, cont_inf_HCW]
        # if TP > 100:
        #     TP = TP*0.001
        TP = TP*TP_pyth
        TP = TP * Labor_fact * HEAD_Labor
        
        for i in range(labor_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_labor_2[i][1] == 0 and V_labor_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_labor_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_labor_2[i][6] = day_current + 1 
                    V_labor_2[i][5] = 'Staff2_LABORATORY'

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_labor_2))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_labor_2[Sus_HCW][1] == 0 and V_labor_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_labor_2[Sus_HCW][3] = day_current + 1
            V_labor_2[Sus_HCW][5] = 'Staff2_LABORATORY' 
            V_labor_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 

    return



def meet_HCW_3():

#---------------------------- TRANS PROB  INIT --------------------------------
# FAR -FIELD
# 1- Count the total of infected HCWs of the area
# 2- Check FF TP for time_area_HCW and appy for each HCW of the area  
#
# NEAR FIELD
# 1- Random select a HCW from area, account for the total of inf from FAR-FIELD
# 2- if suscept, apply NF TP for Prop_H_H_Recep
#
#---------------------------- TRANS PROB BOTOM --------------------------------

    
    #  -------  RECEPTION --------------------
    cont_inf_HCW = 0
    infe_WCH = 0
    for i in range(recep_N_s3):
        if V_recep_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH = V_recep_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Recep_fact
        
        for i in range(recep_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_recep_3[i][1] == 0 and V_recep_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_recep_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_recep_3[i][6] = day_current + 1 
                    V_recep_3[i][5] = 'Staff3_RECEPTION' 
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_recep_3))-1 )
    if ( (infe_WCH != 0) and  
            (V_recep_3[Sus_HCW][1] == 0 and V_recep_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Recep)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_recep_3[Sus_HCW][3] = day_current + 1
            V_recep_3[Sus_HCW][5] = 'Staff3_RECEPTION' 
            V_recep_3[Sus_HCW][6] = day_current + 1  
     # -----------------  Near Field H-H  close  ------------------------
    

    #  -------  TRIAGE --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(triag_N_s3):
        if V_triag_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_triag_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Triag_fact
        for i in range(triag_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_triag_3[i][1] == 0 and V_triag_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_triag_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_triag_3[i][6] = day_current + 1 
                    V_triag_3[i][5] = 'Staff3_TRIAGE'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_triag_3))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_triag_3[Sus_HCW][1] == 0 and V_triag_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Triag)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_triag_3[Sus_HCW][3] = day_current + 1
            V_triag_3[Sus_HCW][5] = 'Staff3_TRIAGE' 
            V_triag_3[Sus_HCW][6] = day_current + 1 
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  ATTEN_URGE --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s3):
        if V_nurse_No_Urg_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_3[i])
    for i in range(Dr_NU_s3):
        if dr_No_Urg_V_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_3[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        TP = Tr_Pr['6_Atte_Urg_1'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Att_U_fact * HEAD_Att_U
        for i in range(nur_NU_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_3[i][6] = day_current + 1 
                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTEN_URGE' 
        for i in range(Dr_NU_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_3[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_3[i][6] = day_current + 1 
                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTEN_URGE'    
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_3))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTEN_URGE' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTEN_URGE' 
        if ((random.random() < TP) and (dr_No_Urg_V_3[Sus_M][1] == 0) and
            (dr_No_Urg_V_3[Sus_M][6] == 0) ):
            dr_No_Urg_V_3[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_3[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_3[Sus_M][5] = 'Staff3_ATTEN_URGE' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  ATTE_N_URG --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s3):
        if V_nurse_No_Urg_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_3[i])
    for i in range(Dr_NU_s3):
        if dr_No_Urg_V_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_3[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        
        if CURTAINS_INTRV:
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth*CURTAINS
        # else: 
        #     TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
            TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, cont_inf_HCW]*TP_pyth
        else: 
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        
        # TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Att_N_fact * HEAD_Att_NU
        # TP = TP*ATT_NU_H_H
        for i in range(nur_NU_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_3[i][6] = day_current + 1 
                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTE_N_URG' 
        for i in range(Dr_NU_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_3[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_3[i][6] = day_current + 1 
                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG' 
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_3))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTE_N_URG' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTE_N_URG' 
        if ((random.random() < TP) and (dr_No_Urg_V_3[Sus_M][1] == 0) and
            (dr_No_Urg_V_3[Sus_M][6] == 0) ):
            dr_No_Urg_V_3[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_3[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_3[Sus_M][5] = 'Staff3_ATTE_N_URG' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  IMAGING --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(imagi_N):
        if V_imagin_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_imagin_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['7_Imaging'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['7_Imaging'].loc[index, cont_inf_HCW]
        # if TP > 100:
        #     TP = TP*0.001
        TP = TP * Imagi_fact * HEAD_Imag
        TP = TP*TP_pyth
        
        for i in range(imagi_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_imagin_3[i][1] == 0 and V_imagin_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_imagin_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_imagin_3[i][6] = day_current + 1 
                    V_imagin_3[i][5] = 'Staff3_IMAGING'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_imagin_3))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_imagin_3[Sus_HCW][1] == 0 and V_imagin_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index,
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_imagin_3[Sus_HCW][3] = day_current + 1
            V_imagin_3[Sus_HCW][5] = 'Staff3_IMAGING' 
            V_imagin_3[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  LABORATORY --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(labor_N):
        if V_labor_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_labor_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['8_Laborat'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['8_Laborat'].loc[index, cont_inf_HCW]
        # if TP > 100:
        #     TP = TP*0.001
        TP = TP*TP_pyth
        TP = TP * Labor_fact * HEAD_Labor
        
        for i in range(labor_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_labor_3[i][1] == 0 and V_labor_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_labor_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_labor_3[i][6] = day_current + 1 
                    V_labor_3[i][5] = 'Staff3_LABORATORY'

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_labor_3))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_labor_3[Sus_HCW][1] == 0 and V_labor_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_labor_3[Sus_HCW][3] = day_current + 1
            V_labor_3[Sus_HCW][5] = 'Staff3_LABORATORY' 
            V_labor_3[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 


    return



def main_funct():
    global Time_var, ROMS_G, BEDS_G
    N_new_day_from_w = []
    N_new_day_work = []
    N_new_day = []
    N_waiting_H = []
    
    Result_worker = []
    
    N_new_day_from_shift_1 = []
    N_new_day_from_shift_2 = []
    N_new_day_from_shift_3 = []
    
    HCW_inf_1 = []
    HCW_inf_2 = []
    HCW_inf_3 = []
    
    port_RECEP_from_shift_1  =[]
    port_TRIAG_from_shift_1 =[]
    port_TRIAG_U_from_shift_1  =[]
    port_N_URG_from_shift_1 =[]
    port_N_N_URG_from_shift_1  =[]
    port_DR_URGE_from_shift_1  =[]
    port_DR_N_URG_from_shift_1 =[]
    port_IMAGI_from_shift_1 =[]
    port_LABOR_from_shift_1 =[]
    port_ARE_test_from_shift_1 =[]
    
    port_RECEP_from_shift_2  =[]
    port_TRIAG_from_shift_2 =[]
    port_TRIAG_U_from_shift_2  =[]
    port_N_URG_from_shift_2 =[]
    port_N_N_URG_from_shift_2  =[]
    port_DR_URGE_from_shift_2  =[]
    port_DR_N_URG_from_shift_2 =[]
    port_IMAGI_from_shift_2 =[]
    port_LABOR_from_shift_2 =[]
    port_ARE_test_from_shift_2 =[]
    
    port_RECEP_from_shift_3  =[]
    port_TRIAG_from_shift_3 =[]
    port_TRIAG_U_from_shift_3  =[]
    port_N_URG_from_shift_3 =[]
    port_N_N_URG_from_shift_3  =[]
    port_DR_URGE_from_shift_3  =[]
    port_DR_N_URG_from_shift_3 =[]
    port_IMAGI_from_shift_3 =[]
    port_LABOR_from_shift_3 =[]
    port_ARE_test_from_shift_3 =[]
    
    
    
    RECEP_from_shift_1 = []
    TRIAG_from_shift_1 = []
    TRIAG_U_from_shift_1 = []
    N_URG_from_shift_1 = []
    N_N_URG_from_shift_1 = []
    IMAGI_from_shift_1 = []
    LABOR_from_shift_1 = []
    DR_URGE_from_shift_1 = []
    DR_N_URG_from_shift_1 = []
    ARE_test_from_shift_1 = []
                           
    RECEP_from_shift_2 = []
    TRIAG_from_shift_2 = []
    TRIAG_U_from_shift_2 = []
    N_URG_from_shift_2 = []
    N_N_URG_from_shift_2 = []
    IMAGI_from_shift_2 = []
    LABOR_from_shift_2 = []
    DR_URGE_from_shift_2 = []
    DR_N_URG_from_shift_2 = []
    ARE_test_from_shift_2 = []
    
    RECEP_from_shift_3 = []
    TRIAG_from_shift_3 = []
    TRIAG_U_from_shift_3 = []
    N_URG_from_shift_3 = []
    N_N_URG_from_shift_3 = []
    IMAGI_from_shift_3 = []
    LABOR_from_shift_3 = []
    DR_URGE_from_shift_3 = []
    DR_N_URG_from_shift_3 = []
    ARE_test_from_shift_3 = []
    
    Recep_port = []
    Triag_port = []
    WaitU_port = []
    WaitN_port = []
    AtteU_port = []
    AtteN_port = []
    Imagi_port = []
    Labot_port = []
    
    Recep_port_HCW = []
    Triag_port_HCW = []
    AtteU_port_HCW = []
    AtteN_port_HCW = []
    Imagi_port_HCW = []
    Labot_port_HCW = []
    Base1_port_HCW = []
    Base2_port_HCW = []
    Base3_port_HCW = []
    
    Recep_propo = 0
    Triag_propo = 0
    WaitU_propo = 0
    WaitN_propo = 0
    AtteU_propo = 0
    AtteN_propo = 0
    Imagi_propo = 0
    Labot_propo = 0
    
    Recep_prop_H = 0
    Triag_prop_H = 0
    AtteU_prop_H = 0
    AtteN_prop_H = 0
    Imagi_prop_H = 0
    Labot_prop_H = 0
    Base1_prop_H = 0
    Base2_prop_H = 0
    Base3_prop_H = 0
    
     
    Result_user = []
    result_monthly = []

    nday  = N_days
    for day in range(nday):
        day_current = day
        arrival_method(Time_var)
        
        day_inf = day_cases[day_current]
        if day_inf > 0:
            infec = np.random.randint(1,len(Users), size=(day_inf))

            for i in range(len(infec)):
                Users[infec[i]][1] = 1
                Users[infec[i]][9] = INFEC
        
        if WAIT_NU_INTRV:
            for i in range(len(Users)):
                if Users[i][2] == 'RECEPTION':
                    ROOM_W = np.random.randint(1,3) # patient to room 1 or 2 in WNU
                    if 1 == ROOM_W:
                        Users[i][13] = 'WAT_ROM_1'
                    else:
                        Users[i][13] = 'WAT_ROM_2'
            
        while Time_var < Time_scale:
            # if (Time_var >= shift_1[0]) and (Time_var <= shift_1[1]):
                # arrival_method(Time_var)
            for k in range(len(Users)):
                if Users[k][5] == Time_var:
                    Users[k][4] = 1
                    
                if (Users[k][5] < Time_var) and (Users[k][4] < Users[k][3]):
                    Curr_time = Users[k][4]
                    Users[k][4] = Curr_time + 1
                    
                if (Users[k][4] == Users[k][3]) and (Users[k][5] < Time_var):  
                    # area time counter = area time
                    action_desit_tree(Users[k], k, day, Time_var)         
                    area_desit_tree(Users[k],k)
            
            
            # ---------- HWC MEETING PER AREA IN NORMAL WORK END SHIFTS ------
            
            # if shift_1[0] == Time_var:
            #     meet_HCW_1()
            
            # if shift_2[0] == Time_var:
            #     meet_HCW_2()
                
            # if shift_3[0] == Time_var:
            #     meet_HCW_3()
    
            
            #SCREE_HCW 
            # if (shift_2[0] == Time_var and SCREE_HCW and day_current > 9):
            #     Users_workers_shift_1 = []
            #     Users_workers_shift_2 = []
            #     Users_workers_shift_3 = []
            #     # Create worker_shifts 
            #     staff_shift  = workers_settings(Users_workers_shift_1, 
            #                                     Users_workers_shift_2, 
            #                                     Users_workers_shift_3)
            #     Users_workers_shift_2 = staff_shift[1]
                
            #     for i in range(len(Users_workers_shift_2)):
            #         PCR_test = random.random() < PCR_Eff
            #         if (Users_workers_shift_2[i][1] != 0 
            #             and (PCR_test)):
            #             Users_workers_shift_2[i][8] = REPLACE
            #             Users_workers_shift_2[i][1] = 0
            #             Users_workers_shift_2[i][4] = 0
            #             Users_workers_shift_2[i][5] = UNDEF
            #             Users_workers_shift_2[i][6] = 0
            #             Users_workers_shift_2[i][7] = UNDEF
            #             Users_workers_shift_2[i][9] = UNDEF
            #             Users_workers_shift_2[i][10] = UNDEF
            #             Users_workers_shift_2[i][11] = 0
            #             Users_workers_shift_2[i][12] = 0
            #             #Users_workers_shift_1[i][13] = 0
            #             Users_workers_shift_2[i][14] = UNDEF
            
            if shift_2[0] == Time_var:
                meet_HCW_2()
            # --------- HCW REPORTING (Pflegestützpunkt) SHIFT 1 and 2  -------   
            if Time_var == shift_2[0]:
                N_HCW_inf_tot = 0
                N_HCW_inf_1 = 0
                N_HCW_inf_2 = 0
                Users_workers_shift_1 = []
                Users_workers_shift_2= []
                Users_workers_shift_3= []
                # Create worker_shifts 
                staff_shift  = workers_settings(Users_workers_shift_1, 
                                                Users_workers_shift_2, 
                                                Users_workers_shift_3)
                Users_workers_shift_1 = staff_shift[0]
                Users_workers_shift_2 = staff_shift[1]
                # Users_workers_shift_3 = staff_shift[2]
                
                # ------- Interv SPLIT Burse base
                # 1- Size of both HCWs groups of the shift
                # 2. From size, rand select half of each group to meet the other
                #    rand half or the other group
                # 3. For each half, apply room characterit.
                
                # NB_SPLIT = 1
                if NB_SPLIT:
                    ROOM_1 = 1
                    ROOM_2 = 1            
                    
                    G_1 = random.sample(range(0, len(Users_workers_shift_1)), 
                                        (int((len(Users_workers_shift_1))/2)) )
                    G_2 = random.sample(range(0, len(Users_workers_shift_2)), 
                                        (int((len(Users_workers_shift_2))/2)) )
                    
                    G_H_1 = []
                    G_H_1_2 = []
                    G_H_2 = []
                    G_H_2_2 = []
                    for i in range(len(G_1)):
                        G_H_1.append((Users_workers_shift_1[G_1[i]]))
                    for i in range(len(Users_workers_shift_1)):
                        if (not(Users_workers_shift_1[i] in G_H_1)):
                            G_H_1_2.append(Users_workers_shift_1[i])
                    
                    for i in range(len(G_2)):
                        G_H_2.append((Users_workers_shift_2[G_2[i]]))
                    for i in range(len(Users_workers_shift_2)):
                        if (not(Users_workers_shift_2[i] in G_H_2)):
                            G_H_2_2.append(Users_workers_shift_2[i])
                    
                    # ---- ROOM 1
                    if ROOM_1:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_1)):
                            if G_H_1[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_1[i])
                        for i in range(len(G_H_2)):
                            if G_H_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        # print(N_HCW_inf_tot)
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                         N_HCW_inf_tot]*TP_pyth
                            TP = TP * Nur_B_fact
                            TP = TP * T_NB
           
                            for i in range(len(G_H_1)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_1[i][1] == 0 and 
                                        G_H_1[i][6] == 0):
                                        i_n = Users_workers_shift_1.index(G_H_1[i])
                                        Users_workers_shift_1[i_n][3] = day_current + 1 
                                        Users_workers_shift_1[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE'
                          
                            for i in range(len(G_H_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_2[i][1] == 0 and 
                                        G_H_2[i][6] == 0):
                                        i_n = Users_workers_shift_2.index(G_H_2[i])
                                        Users_workers_shift_2[i_n][3] = day_current + 1 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2)-1)
                                if (G_H_2[Sus_2][1] == 0 and 
                                                    G_H_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                            Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_1)-1)
                                if (G_H_1[Sus_1][1] == 0 and 
                                                    G_H_1[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_1.index(G_H_1[Sus_1])
                                        Users_workers_shift_1[i_n][3] = day_current + 1
                                        Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_1[i_n][6] = day_current + 1
                        
                    #    ----------  Close Near Field  ----------------------------

                    # ---- ROOM 2
                    if ROOM_2:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_1_2)):
                            if G_H_1_2[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_1_2[i])
                        for i in range(len(G_H_2_2)):
                            if G_H_2_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        # print(N_HCW_inf_tot)
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                                TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                             N_HCW_inf_tot]*TP_pyth
                                TP = TP * Nur_B_fact
                                TP = TP * T_NB
               
                                for i in range(len(G_H_1_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_1_2[i][1] == 0 and 
                                            G_H_1_2[i][6] == 0):
                                            i_n = Users_workers_shift_1.index(G_H_1_2[i])
                                            Users_workers_shift_1[i_n][3] = day_current + 1 
                                            Users_workers_shift_1[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE'
                              
                                for i in range(len(G_H_2_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_2_2[i][1] == 0 and 
                                            G_H_2_2[i][6] == 0):
                                            i_n = Users_workers_shift_2.index(G_H_2_2[i])
                                            Users_workers_shift_2[i_n][3] = day_current + 1 
                                            Users_workers_shift_2[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2_2)-1)
                                if (G_H_2_2[Sus_2][1] == 0 and 
                                                    G_H_2_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                            Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_1_2)-1)
                                if (G_H_1_2[Sus_1][1] == 0 and 
                                                    G_H_1_2[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_1.index(G_H_1_2[Sus_1])
                                        Users_workers_shift_1[i_n][3] = day_current + 1
                                        Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_1[i_n][6] = day_current + 1
                                        
                    #    ----------  Close Near Field  ----------------------------  
                
                else:
                
                    Inf_H_1 = []
                    Inf_H_2 = []
                    for i in range(len(Users_workers_shift_1)):
                        if Users_workers_shift_1[i][1] == 1:
                            N_HCW_inf_1 = N_HCW_inf_1 + 1
                            Inf_H_1.append(Users_workers_shift_1[i])
                    for i in range(len(Users_workers_shift_2)):
                        if Users_workers_shift_2[i][1] == 1:
                            N_HCW_inf_2 = N_HCW_inf_2 + 1
                            Inf_H_2.append(Users_workers_shift_2[i])
                    N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                    if N_HCW_inf_tot:
                        TP_major = 1
                        if N_HCW_inf_tot > 9:
                            N_HCW_inf_tot = 9
                            TP_major = 3
                         
                        # if HCW_BASES:
                        #     if N_HCW_inf_tot > 5:
                        #         N_HCW_inf_tot = 5
                        
                        if NB_ROOM:
                            if N_HCW_inf_tot > 5:
                                N_HCW_inf_tot = 5                           
                            TP = Tr_Pr['8_Laborat'].loc[7, N_HCW_inf_tot]
                            TP = TP * Labor_fact
                            # TP = TP*TP_pyth*TP_major
                            TP = TP*TP_pyth*1
                            TP_major = 1
                            
                        else:
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                     N_HCW_inf_tot]*TP_pyth
                            TP = TP * Nur_B_fact
                            TP = TP * T_NB
                        for i in range(len(Users_workers_shift_1)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if (Users_workers_shift_1[i][1] == 0 and 
                                    Users_workers_shift_1[i][6] == 0):
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_1[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_1[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff2_HCW_BASE'
                      
                        for i in range(len(Users_workers_shift_2)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if (Users_workers_shift_2[i][1] == 0 and 
                                    Users_workers_shift_2[i][6] == 0):
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_2[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_2[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff2_HCW_BASE'
                
                    # ------------- Nurse Base - Near field
                    if len(Inf_H_1) > 0:
                        Sus_2 = random.randint(0, len(Users_workers_shift_2)-1)
                        if (Users_workers_shift_2[Sus_2][1] == 0 and 
                                            Users_workers_shift_2[Sus_2][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_2[Sus_2][3] = day_current + 1
                                Users_workers_shift_2[Sus_2][5] = 'Staff1_HCW_BASE' 
                                Users_workers_shift_2[Sus_2][6] = day_current + 1 
                    if len(Inf_H_2) > 0:
                        Sus_1 = random.randint(0, len(Users_workers_shift_1)-1)
                        if (Users_workers_shift_1[Sus_1][1] == 0 and 
                                            Users_workers_shift_1[Sus_1][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            TP = Tr_Pr_NEAR['Near'].loc[index, 
                                        Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_1[Sus_1][3] = day_current + 1
                                Users_workers_shift_1[Sus_1][5] = 'Staff2_HCW_BASE' 
                                Users_workers_shift_1[Sus_1][6] = day_current + 1
                    #    ----------  Close Near Field  ----------------------------
                    
            # --------- HCW REPORTING (Pflegestützpunkt) SHIFT 2 and 3  -------
            # if (shift_3[0] == Time_var and SCREE_HCW and day_current > 9):
            #     Users_workers_shift_1 = []
            #     Users_workers_shift_2 = []
            #     Users_workers_shift_3 = []
            #     # Create worker_shifts 
            #     staff_shift  = workers_settings(Users_workers_shift_1, 
            #                                     Users_workers_shift_2, 
            #                                     Users_workers_shift_3)
            #     Users_workers_shift_3 = staff_shift[2]
                
            #     for i in range(len(Users_workers_shift_3)):
            #         PCR_test = random.random() < PCR_Eff
            #         if (Users_workers_shift_3[i][1] != 0 
            #             and (PCR_test)):
            #             # and Users_workers_shift_2[i][9] == 'infectious'):
            #             Users_workers_shift_3[i][8] = REPLACE
            #             Users_workers_shift_3[i][1] = 0
            #             Users_workers_shift_3[i][4] = 0
            #             Users_workers_shift_3[i][5] = UNDEF
            #             Users_workers_shift_3[i][6] = 0
            #             Users_workers_shift_3[i][7] = UNDEF
            #             Users_workers_shift_3[i][9] = UNDEF
            #             Users_workers_shift_3[i][10] = UNDEF
            #             Users_workers_shift_3[i][11] = 0
            #             Users_workers_shift_3[i][12] = 0
            #             Users_workers_shift_3[i][14] = UNDEF
            
            if shift_3[0] == Time_var:
                meet_HCW_3()
            
            if Time_var == shift_3[0]:
                N_HCW_inf_tot = 0
                N_HCW_inf_2 = 0
                N_HCW_inf_3 = 0
                Users_workers_shift_1 = []
                Users_workers_shift_2= []
                Users_workers_shift_3= []
                # Create worker_shifts 
                staff_shift  = workers_settings(Users_workers_shift_1, 
                                                Users_workers_shift_2, 
                                                Users_workers_shift_3)
                Users_workers_shift_1 = staff_shift[0]
                Users_workers_shift_2 = staff_shift[1]
                Users_workers_shift_3 = staff_shift[2]
                
                # ------- Interv SPLIT Burse base
                # 1- Size of both HCWs groups of the shift
                # 2. From size, rand select half of each group to meet the other
                #    rand half or the other group
                # 3. For each half, apply room characterit.
                
                if NB_SPLIT:
                    ROOM_1 = 1
                    ROOM_2 = 1
                    
                    G_3 = random.sample(range(0, len(Users_workers_shift_3)), 
                                        (int((len(Users_workers_shift_3))/2)) )
                    G_2 = random.sample(range(0, len(Users_workers_shift_2)), 
                                        (int((len(Users_workers_shift_2))/2)) )
                    
                    G_H_3 = []
                    G_H_3_2 = []
                    G_H_2 = []
                    G_H_2_2 = []
                    for i in range(len(G_3)):
                        G_H_3.append((Users_workers_shift_3[G_3[i]]))
                    for i in range(len(Users_workers_shift_3)):
                        if (not(Users_workers_shift_3[i] in G_H_3)):
                            G_H_3_2.append(Users_workers_shift_3[i])
                    
                    for i in range(len(G_2)):
                        G_H_2.append((Users_workers_shift_2[G_2[i]]))
                    for i in range(len(Users_workers_shift_2)):
                        if (not(Users_workers_shift_2[i] in G_H_2)):
                            G_H_2_2.append(Users_workers_shift_2[i])
                    
                    # ---- ROOM 1
                    if ROOM_1:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3)):
                            if G_H_3[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3[i])
                        for i in range(len(G_H_2)):
                            if G_H_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                         N_HCW_inf_tot]*TP_pyth
                            TP = TP * Nur_B_fact
                            TP = TP * T_NB
           
                            for i in range(len(G_H_3)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_3[i][1] == 0 and 
                                        G_H_3[i][6] == 0):
                                        i_n = Users_workers_shift_3.index(G_H_3[i])
                                        Users_workers_shift_3[i_n][3] = day_current + 1 
                                        Users_workers_shift_3[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff3_HCW_BASE'
                          
                            for i in range(len(G_H_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_2[i][1] == 0 and 
                                        G_H_2[i][6] == 0):
                                        i_n = Users_workers_shift_2.index(G_H_2[i])
                                        Users_workers_shift_2[i_n][3] = day_current + 1 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff3_HCW_BASE'
                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2)-1)
                                if (G_H_2[Sus_2][1] == 0 and 
                                                    G_H_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                            Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff3_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_3)-1)
                                if (G_H_3[Sus_1][1] == 0 and 
                                                    G_H_3[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_3.index(G_H_3[Sus_1])
                                        Users_workers_shift_3[i_n][3] = day_current + 1
                                        Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_3[i_n][6] = day_current + 1
                        
                    #    ----------  Close Near Field  ----------------------------

                    # ---- ROOM 2
                    if ROOM_2:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3_2)):
                            if G_H_3_2[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3_2[i])
                        for i in range(len(G_H_2_2)):
                            if G_H_2_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                         N_HCW_inf_tot]*TP_pyth
                            TP = TP * Nur_B_fact
                            TP = TP * T_NB
           
                            for i in range(len(G_H_3_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_3_2[i][1] == 0 and 
                                        G_H_3_2[i][6] == 0):
                                        i_n = Users_workers_shift_3.index(G_H_3_2[i])
                                        Users_workers_shift_3[i_n][3] = day_current + 1 
                                        Users_workers_shift_3[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE'
                          
                            for i in range(len(G_H_2_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_2_2[i][1] == 0 and 
                                        G_H_2_2[i][6] == 0):
                                        i_n = Users_workers_shift_2.index(G_H_2_2[i])
                                        Users_workers_shift_2[i_n][3] = day_current + 1 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                                        
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2_2)-1)
                                if (G_H_2_2[Sus_2][1] == 0 and 
                                                    G_H_2_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                            Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_3_2)-1)
                                if (G_H_3_2[Sus_1][1] == 0 and 
                                                    G_H_3_2[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_3.index(G_H_3_2[Sus_1])
                                        Users_workers_shift_3[i_n][3] = day_current + 1
                                        Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_3[i_n][6] = day_current + 1
                                        
                    #    ----------  Close Near Field  ----------------------------  
                
                
                else:
                    N_HCW_inf_tot = 0
                    N_HCW_inf_2 = 0
                    N_HCW_inf_3 = 0
                    Users_workers_shift_1 = []
                    Users_workers_shift_2= []
                    Users_workers_shift_3= []
                    # Create worker_shifts 
                    staff_shift  = workers_settings(Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3)
                    Users_workers_shift_1 = staff_shift[0]
                    Users_workers_shift_2 = staff_shift[1]
                    Users_workers_shift_3 = staff_shift[2]
                    
                    Inf_H_2 = []
                    Inf_H_3 = []
                    for i in range(len(Users_workers_shift_2)):
                        if Users_workers_shift_2[i][1] == 1:
                            N_HCW_inf_2 = N_HCW_inf_2 + 1
                            Inf_H_2.append(Users_workers_shift_2[i])
                    for i in range(len(Users_workers_shift_3)):
                        if Users_workers_shift_3[i][1] == 1:
                            N_HCW_inf_3 = N_HCW_inf_3 + 1
                            Inf_H_3.append(Users_workers_shift_3[i])
                    N_HCW_inf_tot = N_HCW_inf_2 + N_HCW_inf_3
                    if N_HCW_inf_tot:
                        TP_major = 1
                        if N_HCW_inf_tot > 9:
                            N_HCW_inf_tot = 9
                            TP_major = 3
                            
                        # if HCW_BASES:
                        #     if N_HCW_inf_tot > 5:
                        #         N_HCW_inf_tot = 5
                                
                        if NB_ROOM:
                            if N_HCW_inf_tot > 5:
                                N_HCW_inf_tot = 5                           
                            TP = Tr_Pr['8_Laborat'].loc[7, N_HCW_inf_tot]
                            TP = TP * Labor_fact
                            # TP = TP*TP_pyth*TP_major
                            TP = TP*TP_pyth*1
                            TP_major = 1
                            
                        else:
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                     N_HCW_inf_tot]*TP_pyth
                            TP = TP * Nur_B_fact
                            TP = TP * T_NB
                        for i in range(len(Users_workers_shift_2)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_2[i][1] == 0 and Users_workers_shift_2[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_2[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_2[i][6] = day_current + 1 
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff2_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff3_HCW_BASE'
                      
                        for i in range(len(Users_workers_shift_3)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_3[i][1] == 0 and Users_workers_shift_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_3[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_3[i][6] = day_current + 1 
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff2_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff3_HCW_BASE'
    
                    # ------------- Nurse Base - Near field
                    if len(Inf_H_2) > 0:
                        Sus_2 = random.randint(0, len(Users_workers_shift_2)-1)
                        if (Users_workers_shift_2[Sus_2][1] == 0 and 
                                            Users_workers_shift_2[Sus_2][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_2[Sus_2][3] = day_current + 1
                                Users_workers_shift_2[Sus_2][5] = 'Staff3_HCW_BASE' 
                                Users_workers_shift_2[Sus_2][6] = day_current + 1 
                    if len(Inf_H_3) > 0:
                        Sus_1 = random.randint(0, len(Users_workers_shift_3)-1)
                        if (Users_workers_shift_3[Sus_1][1] == 0 and 
                                            Users_workers_shift_3[Sus_1][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_3[Sus_1][3] = day_current + 1
                                Users_workers_shift_3[Sus_1][5] = 'Staff2_HCW_BASE' 
                                Users_workers_shift_3[Sus_1][6] = day_current + 1
                    #  ------------  Close Near Field  ----------------------------
            
            # --------- HCW REPORTING (Pflegestützpunkt) SHIFT 3 and 1  -------
            
            # if (shift_1[0] == Time_var and SCREE_HCW and day_current > 9):
            #     Users_workers_shift_1 = []
            #     Users_workers_shift_2 = []
            #     Users_workers_shift_3 = []
            #     # Create worker_shifts 
            #     staff_shift  = workers_settings(Users_workers_shift_1, 
            #                                     Users_workers_shift_2, 
            #                                     Users_workers_shift_3)
            #     Users_workers_shift_1 = staff_shift[0]
                
            #     for i in range(len(Users_workers_shift_1)):
            #         PCR_test = random.random() < PCR_Eff
            #         if (Users_workers_shift_1[i][1] != 0 
            #             and (PCR_test)):
            #             # and Users_workers_shift_2[i][9] == 'infectious'):
            #             Users_workers_shift_1[i][8] = REPLACE
            #             Users_workers_shift_1[i][1] = 0
            #             Users_workers_shift_1[i][4] = 0
            #             Users_workers_shift_1[i][5] = UNDEF
            #             Users_workers_shift_1[i][6] = 0
            #             Users_workers_shift_1[i][7] = UNDEF
            #             Users_workers_shift_1[i][9] = UNDEF
            #             Users_workers_shift_1[i][10] = UNDEF
            #             Users_workers_shift_1[i][11] = 0
            #             Users_workers_shift_1[i][12] = 0
            #             Users_workers_shift_1[i][14] = UNDEF
            
            
            if shift_1[0] == Time_var:
                meet_HCW_1()
            
            if Time_var == shift_1[0]:
             
                if NB_SPLIT:
                    N_HCW_inf_tot = 0
                    N_HCW_inf_1 = 0
                    N_HCW_inf_3 = 0
                    Users_workers_shift_1 = []
                    Users_workers_shift_2= []
                    Users_workers_shift_3= []
                    # Create worker_shifts 
                    staff_shift  = workers_settings(Users_workers_shift_1, 
                                 Users_workers_shift_2, Users_workers_shift_3)
                    Users_workers_shift_1 = staff_shift[0]
                    Users_workers_shift_2 = staff_shift[1]
                    Users_workers_shift_3 = staff_shift[2]
                    
                    ROOM_1 = 1
                    ROOM_2 = 1
                    
                    G_3 = random.sample(range(0, len(Users_workers_shift_3)), 
                                        (int((len(Users_workers_shift_3))/2)) )
                    G_1 = random.sample(range(0, len(Users_workers_shift_1)), 
                                        (int((len(Users_workers_shift_1))/2)) )
                    
                    G_H_3 = []
                    G_H_3_2 = []
                    G_H_1 = []
                    G_H_1_2 = []
                    for i in range(len(G_3)):
                        G_H_3.append((Users_workers_shift_3[G_3[i]]))
                    for i in range(len(Users_workers_shift_3)):
                        if (not(Users_workers_shift_3[i] in G_H_3)):
                            G_H_3_2.append(Users_workers_shift_3[i])
                    
                    for i in range(len(G_1)):
                        G_H_1.append((Users_workers_shift_1[G_1[i]]))
                    for i in range(len(Users_workers_shift_1)):
                        if (not(Users_workers_shift_1[i] in G_H_1)):
                            G_H_1_2.append(Users_workers_shift_1[i])
                    
                    # ---- ROOM 1
                    if ROOM_1:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3)):
                            if G_H_3[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3[i])
                        for i in range(len(G_H_1)):
                            if G_H_1[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_1[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            
                            if NB_ROOM:
                                if N_HCW_inf_tot > 5:
                                    N_HCW_inf_tot = 5                           
                                TP = Tr_Pr['8_Laborat'].loc[7, N_HCW_inf_tot]
                                TP = TP * Labor_fact
                                TP = TP*TP_pyth
                                
                            else:
                                TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                         N_HCW_inf_tot]*TP_pyth
                                TP = TP * Nur_B_fact
                                TP = TP * T_NB
           
                            for i in range(len(G_H_3)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_3[i][1] == 0 and 
                                        G_H_3[i][6] == 0):
                                        i_n = Users_workers_shift_3.index(G_H_3[i])
                                        Users_workers_shift_3[i_n][3] = day_current + 1 
                                        Users_workers_shift_3[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff3_HCW_BASE'
                          
                            for i in range(len(G_H_1)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_1[i][1] == 0 and 
                                        G_H_1[i][6] == 0):
                                        i_n = Users_workers_shift_1.index(G_H_1[i])
                                        Users_workers_shift_1[i_n][3] = day_current + 1 
                                        Users_workers_shift_1[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE'
                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_1)-1)
                                if (G_H_1[Sus_2][1] == 0 and 
                                                    G_H_1[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                            Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_1.index(G_H_1[Sus_2])
                                        Users_workers_shift_1[i_n][3] = day_current + 1
                                        Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE' 
                                        Users_workers_shift_1[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_3)-1)
                                if (G_H_3[Sus_1][1] == 0 and 
                                                    G_H_3[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_3.index(G_H_3[Sus_1])
                                        Users_workers_shift_3[i_n][3] = day_current + 1
                                        Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_3[i_n][6] = day_current + 1
                        
                    #    ----------  Close Near Field  ----------------------------

                    # ---- ROOM 2
                    if ROOM_2:
                        
                        G_H_2_2 = G_H_1_2
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3_2)):
                            if G_H_3_2[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3_2[i])
                        for i in range(len(G_H_2_2)):
                            if G_H_2_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                                TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                             N_HCW_inf_tot]*TP_pyth
                                TP = TP * Nur_B_fact
                                TP = TP * T_NB
               
                                for i in range(len(G_H_3_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_3_2[i][1] == 0 and 
                                            G_H_3_2[i][6] == 0):
                                            i_n = Users_workers_shift_3.index(G_H_3_2[i])
                                            Users_workers_shift_3[i_n][3] = day_current + 1 
                                            Users_workers_shift_3[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_3[i_n][5] = 'Staff3_HCW_BASE'
                              
                                for i in range(len(G_H_2_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_2_2[i][1] == 0 and 
                                            G_H_2_2[i][6] == 0):
                                            i_n = Users_workers_shift_1.index(G_H_2_2[i])
                                            Users_workers_shift_1[i_n][3] = day_current + 1 
                                            Users_workers_shift_1[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE'
                                            
                                # ------------- Nurse Base - Near field
                                if N_HCW_inf_1 > 0:
                                    Sus_2 = random.randint(0, len(G_H_2_2)-1)
                                    if (G_H_2_2[Sus_2][1] == 0 and 
                                                        G_H_2_2[Sus_2][6] == 0):
                                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                        diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                        index = diff.argmin()
                                        # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                Mask[random.randint(0, 1)]]*TP_pyth_Near
                                        Trnasmiss = random.random() < TP
                                        if Trnasmiss:
                                            i_n = Users_workers_shift_1.index(G_H_2_2[Sus_2])
                                            Users_workers_shift_1[i_n][3] = day_current + 1
                                            Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE' 
                                            Users_workers_shift_1[i_n][6] = day_current + 1 
                                
                                if N_HCW_inf_2 > 0:
                                    Sus_1 = random.randint(0, len(G_H_3_2)-1)
                                    if (G_H_3_2[Sus_1][1] == 0 and 
                                                        G_H_3_2[Sus_1][6] == 0):
                                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                        diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                        index = diff.argmin()
                                        # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                        TP = Tr_Pr_NEAR['Near'].loc[index, 
                                                    Mask[random.randint(0, 1)]]*TP_pyth_Near
                                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                        Trnasmiss = random.random() < TP
                                        if Trnasmiss:
                                            i_n = Users_workers_shift_3.index(G_H_3_2[Sus_1])
                                            Users_workers_shift_3[i_n][3] = day_current + 1
                                            Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE' 
                                            Users_workers_shift_3[i_n][6] = day_current + 1
                                            
                        #    ----------  Close Near Field  ----------------------------  
                else:
                
                    N_HCW_inf_tot = 0
                    N_HCW_inf_1 = 0
                    N_HCW_inf_3 = 0
                    Users_workers_shift_1 = []
                    Users_workers_shift_2= []
                    Users_workers_shift_3= []
                    # Create worker_shifts 
                    staff_shift  = workers_settings(Users_workers_shift_1, 
                                 Users_workers_shift_2, Users_workers_shift_3)
                    Users_workers_shift_1 = staff_shift[0]
                    Users_workers_shift_2 = staff_shift[1]
                    Users_workers_shift_3 = staff_shift[2]
                    
                    Inf_H_1 = []
                    Inf_H_3 = []
                    for i in range(len(Users_workers_shift_1)):
                        if Users_workers_shift_1[i][1] == 1:
                            N_HCW_inf_1 = N_HCW_inf_1 + 1
                            Inf_H_1.append(Users_workers_shift_1[i])
                    for i in range(len(Users_workers_shift_3)):
                        if Users_workers_shift_3[i][1] == 1:
                            N_HCW_inf_3 = N_HCW_inf_3 + 1
                            Inf_H_3.append(Users_workers_shift_3[i])
                    N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_3
                    if N_HCW_inf_tot:
                        TP_major = 1
                        if N_HCW_inf_tot > 9:
                            N_HCW_inf_tot = 9
                            TP_major = 3
                        # if HCW_BASES:
                        #     if N_HCW_inf_tot > 5:
                        #         N_HCW_inf_tot = 5
                        
                        if NB_ROOM:
                            if N_HCW_inf_tot > 5:
                                N_HCW_inf_tot = 5                           
                            TP = Tr_Pr['8_Laborat'].loc[7, N_HCW_inf_tot]
                            TP = TP * Labor_fact
                            TP = TP*TP_pyth*TP_major
                            TP_major = 1
                            
                        else:
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                     N_HCW_inf_tot]*TP_pyth
                            TP = TP * Nur_B_fact
                            TP = TP * T_NB
                        for i in range(len(Users_workers_shift_1)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_1[i][1] == 0 and Users_workers_shift_1[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_1[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_1[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff3_HCW_BASE'
                      
                        for i in range(len(Users_workers_shift_3)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_3[i][1] == 0 and Users_workers_shift_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_3[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_3[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff3_HCW_BASE'
    
                    # ------------- Nurse Base - Near field
                    if len(Inf_H_1) > 0:
                        Sus_2 = random.randint(0, len(Users_workers_shift_1)-1)
                        if (Users_workers_shift_1[Sus_2][1] == 0 and 
                                            Users_workers_shift_1[Sus_2][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_1[Sus_2][3] = day_current + 1
                                Users_workers_shift_1[Sus_2][5] = 'Staff3_HCW_BASE' 
                                Users_workers_shift_1[Sus_2][6] = day_current + 1 
                    if len(Inf_H_3) > 0:
                        Sus_1 = random.randint(0, len(Users_workers_shift_3)-1)
                        if (Users_workers_shift_3[Sus_1][1] == 0 and 
                                            Users_workers_shift_3[Sus_1][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, 'S_SP']
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_3[Sus_1][3] = day_current + 1
                                Users_workers_shift_3[Sus_1][5] = 'Staff1_HCW_BASE' 
                                Users_workers_shift_3[Sus_1][6] = day_current + 1
                    #  ------------  Close Near Field  ----------------------------
            
            Time_var = Time_var + 1
        
        # print(day+1)
        
        for k in range(len(Users)):
            if Users[k][2] != 'EXIT':
                action_desit_tree(Users[k], k, day, 1439) # Same day attendance
                Users[k][8] = Users[k][2]
                Users[k][2] = 'EXIT'
        
        
        Users_workers_shift_1 = []
        Users_workers_shift_2 = []
        Users_workers_shift_3 = []
        
        
        # Create worker_shifts 
        staff_shift  = workers_settings(Users_workers_shift_1, 
                                        Users_workers_shift_2, 
                                        Users_workers_shift_3)
        Users_workers_shift_1 = staff_shift[0]
        Users_workers_shift_2 = staff_shift[1]
        Users_workers_shift_3 = staff_shift[2]
        
        
        cont_1 = 0
        # HCW_inf_1 = []
        for i in range(len(Users_workers_shift_1)):
            if Users_workers_shift_1[i][6] == (day + 1):
                cont_1 = cont_1 + 1
        HCW_inf_1.append([day,cont_1])
        
        cont_2 = 0
        # HCW_inf_2 = []
        for i in range(len(Users_workers_shift_2)):
            if Users_workers_shift_2[i][6] == (day + 1):
                cont_2 = cont_2 + 1
        HCW_inf_2.append([day,cont_2])
        
        cont_3 = 0
        # HCW_inf_3 = []
        for i in range(len(Users_workers_shift_3)):
            if Users_workers_shift_3[i][6] == (day + 1):
                cont_3 = cont_3 + 1
        HCW_inf_3.append([day,cont_3])
            
        
        HCW_propo_num = [Recep_port_HCW,Triag_port_HCW, AtteU_port_HCW,
                         AtteN_port_HCW,Imagi_port_HCW,Labot_port_HCW,
                         Base1_port_HCW, Base2_port_HCW, Base3_port_HCW]    
        
        HCW_propo = proport_HCW_day(day,Users_workers_shift_1,
                                    Users_workers_shift_2,
                                    Users_workers_shift_3,HCW_propo_num)
        
        
        
        #  HCW status - immune | infected | symptoms -
        staff_shift_status = workers_settings_status(Users_workers_shift_1, 
                             Users_workers_shift_2, Users_workers_shift_3, 
                             day_current)
        Users_workers_shift_1 = staff_shift_status[0]
        Users_workers_shift_2 = staff_shift_status[1]
        Users_workers_shift_3 = staff_shift_status[2]
    
        curr_user = Users
        Result_user.extend(curr_user)
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (
                (Users[i][11] == PATIEN+'_RECEPTION') or
                (Users[i][11] == PATIEN+'_TRIAGE') or
                (Users[i][11] == 'WAIT_NO_URGENT') or
                (Users[i][11] == 'WAIT_URGENT') or
                (Users[i][11] == PATIEN+'_ATTEN_URGE') or
                (Users[i][11] == PATIEN+'_ATTE_N_URG') or 
                (Users[i][11] == PATIEN+'_LABORATORY') or 
                (Users[i][11] == PATIEN +'_IMAGING') ) ) :
                cont_use_day = cont_use_day + 1
        N_new_day.append([day,cont_use_day])
        

        User_propo_num = [Recep_port,Triag_port,WaitU_port,WaitN_port,
                          AtteU_port,AtteN_port,Imagi_port,Labot_port]
        User_propot = proport_user_day(day,Users,User_propo_num)
        Recep_port = User_propot[0]
        Triag_port = User_propot[1]
        WaitU_port = User_propot[2]
        WaitN_port = User_propot[3]
        AtteU_port = User_propot[4]
        AtteN_port = User_propot[5]
        Imagi_port = User_propot[6]
        Labot_port = User_propot[7]
        
        
        # if ((day == 10) or (day == 15) or (day == 5) or (day == 20) 
        #     or (day == 3)):
        #     print (day)

        

        """------------------ Patients read next day -------------------------
        """
        if day < len(Aget_day)-1:
            t_arriv = []
            for i in range(hrs):
                pati = int( Df['D'+str(day + 2)].loc[i, "DAY"] )
                if pati > 0:
                    for k in range(pati):
                        t_ar = random.randint(h_ranges[i][0], h_ranges[i][1])   
                        t_arriv.append(t_ar)
                        t_arriv.sort()
                        
                        
            color = ['RED','ORANGE','YELLLOW','GREEN','BLUE','WITHOUT']            
            triag_pat = []
            for i in range(hrs):
                for k in range(len(color)):
                    if (int( Df['D'+str(day + 2)].loc[i,color[k]] )) > 0:
                        for qq in range(int(Df['D'+str(day + 2)].loc[i,
                                                                color[k]])):
                            if ('WITHOUT' == color[k]):
                                k1 = random.randint(2, 4)
                                triag_pat.append(color[k1])
                            else:    
                                triag_pat.append(color[k])

            if len(Users) < Aget_day.loc[day+1, "tot"]:
                tam = Aget_day.loc[day+1, "tot"] - len(Users)
                for i in range(tam):
                    Users.append([i+1, 0, UNDEF, 0, 0, t_arriv[i],0, 0, 
                            UNDEF, UNDEF, 0, UNDEF, UNDEF, UNDEF,
                            UNDEF, UNDEF])
            elif len(Users) > Aget_day.loc[day+1, "tot"]:
                tam = len(Users) - Aget_day.loc[day+1, "tot"]
                for i in range(tam):
                    Users.pop()
            
            # day_users = Users

            for i in range(Aget_day.loc[day+1, "tot"]):
                Users[i] = [i+1, 0, UNDEF, 0, 0, t_arriv[i],0, 0, 
                            UNDEF, UNDEF, 0, UNDEF, triag_pat[i], UNDEF,
                            UNDEF, UNDEF]


            
    

        ROMS_G = []
        for i in range(0, N_rooms_):
            ROMS_G.append(1)

        BEDS_G = []
        for i in range(0, N_beds_):
            BEDS_G.append(1)
    
    
    
        Time_var = 0
    
    #  Counting infected patients by patients and HCW
    Tot_pat = 0
    Tot_HCW = 0
    for i in range(len(User_propot)):
        for k in range(len(Recep_port)):
            Tot_pat = Tot_pat + User_propot[i][k][0]
            Tot_HCW = Tot_HCW + User_propot[i][k][1]     
    Total_patien_inf = Tot_pat + Tot_HCW
    
    #  Counting infected HCW by patients and HCW
    Tot_pat_HCW = 0
    Tot_HCW_HCW = 0
    for i in range(len(HCW_propo)):
        for k in range (len(HCW_propo[i])):
            Tot_pat_HCW = Tot_pat_HCW + HCW_propo[i][k][0]
            Tot_HCW_HCW = Tot_HCW_HCW + HCW_propo[i][k][1]     
    Total_HCW_inf = Tot_pat_HCW + Tot_HCW_HCW
    
    
    
    propo_area = [Recep_propo,Triag_propo,WaitU_propo,WaitN_propo,
                          AtteU_propo,AtteN_propo,Imagi_propo,Labot_propo]
    User_proport = proportion_user_tot(User_propot,propo_area,Total_patien_inf)
    Recep_propo = User_proport[0]
    Triag_propo = User_proport[1]
    WaitU_propo = User_proport[2]
    WaitN_propo = User_proport[3]
    AtteU_propo = User_proport[4]
    AtteN_propo = User_proport[5]
    Imagi_propo = User_proport[6]
    Labot_propo = User_proport[7]
    
    
    propo_HCW = [Recep_prop_H,Triag_prop_H, AtteU_prop_H,AtteN_prop_H,
                  Imagi_prop_H,Labot_prop_H,Base1_prop_H,Base2_prop_H,
                  Base3_prop_H]
    HCWs_proport = propor_HCW_tot(HCW_propo, propo_HCW, Total_HCW_inf)
    Recep_prop_H = HCWs_proport[0]
    Triag_prop_H = HCWs_proport[1]
    AtteU_prop_H = HCWs_proport[2]
    AtteN_prop_H = HCWs_proport[3]
    Imagi_prop_H = HCWs_proport[4]
    Labot_prop_H = HCWs_proport[5]
    Base1_prop_H = HCWs_proport[6]
    Base2_prop_H = HCWs_proport[7]
    Base3_prop_H = HCWs_proport[8]
    
    
    H_coun_by_p = []
    H_coun_by_H = []
    # for i in range(len(HCW_propo)):
    #     for k in range (len(HCW_propo[0])):
            
    for k in range (len(HCW_propo[0])):      
        H_coun_by_p.append( (  HCW_propo[0][k][0] + HCW_propo[1][k][0] +
                               HCW_propo[2][k][0] + HCW_propo[3][k][0] +
                               HCW_propo[4][k][0] + HCW_propo[5][k][0] +
                               HCW_propo[6][k][0] + HCW_propo[7][k][0] +
                               HCW_propo[8][k][0] ) ) 
        H_coun_by_H.append( (  HCW_propo[0][k][1] + HCW_propo[1][k][1] +
                               HCW_propo[2][k][1] + HCW_propo[3][k][1] +
                               HCW_propo[4][k][1] + HCW_propo[5][k][1] +
                               HCW_propo[6][k][1] + HCW_propo[7][k][1] +
                               HCW_propo[8][k][1] ) )
    
    P_coun_by_p = []
    P_coun_by_H = []
    for k in range (len(User_propot[0])):    
        P_coun_by_p.append( ( User_propot[0][k][0] + User_propot[1][k][0] +
                              User_propot[2][k][0] + User_propot[3][k][0] +
                              User_propot[4][k][0] + User_propot[5][k][0] +
                              User_propot[6][k][0] + User_propot[7][k][0] ) )
        P_coun_by_H.append( ( User_propot[0][k][1] + User_propot[1][k][1] +
                              User_propot[2][k][1] + User_propot[3][k][1] +
                              User_propot[4][k][1] + User_propot[5][k][1] +
                              User_propot[6][k][1] + User_propot[7][k][1] ) )
        
    
    
    pat_tot = []
    days_plot = []
    staff_plot = []
    staff_1 = []
    staff_2 = []
    staff_3 = []
    
    HCW_infec_1 = []
    HCW_infec_2 = []
    HCW_infec_3 = []
    for i in range(len(N_new_day)):
        pat_tot.append(N_new_day[i][1])
        # staff_plot.append(cont_from_w_shift_1[i][1] +
        #             cont_from_w_shift_2[i][1] + cont_from_w_shift_3[i][1])
        # staff_1.append(cont_from_w_shift_1[i][1])
        # staff_2.append(cont_from_w_shift_2[i][1])
        # staff_3.append(cont_from_w_shift_3[i][1])
        days_plot.append(N_new_day[i][0]+1)
        HCW_infec_1.append(HCW_inf_1[i][1] + HCW_inf_2[i][1] + HCW_inf_3[i][1])
        HCW_infec_2.append(HCW_inf_2[i][1])
        HCW_infec_3.append(HCW_inf_3[i][1])
    
    
    res_tupple = tuple(tuple(sub) for sub in Users_workers_shift_1)
            
    HCWs_proporttuple = tuple(HCWs_proport)
    User_proporttuple = tuple(User_proport)
    result_monthly.append((User_proporttuple, HCWs_proporttuple, 
                                sum(H_coun_by_p) + sum(H_coun_by_H),
                                sum(P_coun_by_p) + sum(P_coun_by_H),
                               (sum(H_coun_by_p) + sum(H_coun_by_H) +
                                sum(P_coun_by_p) + sum(P_coun_by_H)),
                               res_tupple))
    
    return(result_monthly)
    


Res = main_funct()

# -----------------            EOF