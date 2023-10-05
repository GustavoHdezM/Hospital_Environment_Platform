# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:15:40 2021
    
    Architectural interventions to mitigate the spread of
    SARS-CoV-2 in emergency departments
    
    InnoBRI project 
    This work was supported by the Innovation Funds of the 
    Joint Federal Committee 
    (Innovationsfonds des gemeinsamen Bundesausschusses (G-BA),
     funding reference: 01VSF19032)
    
    Functions file for running platform - NOTE: RUN MAIN FILE
    
@author: Gustavo Hernandez Mejia

"""
# from funct_model_ED_parall import *
import random
import matplotlib.pyplot as plt
import math  
import time
import numpy as np
import pandas as pd
import csv
import statistics

global RECEP, TRIAG, TRIAG, WAI_N, WAI_U,  N_URG, U_URG,IMAGI, LABOR,EXIT_
global AT_UR, At_NU, Users


RECEP = 'RECEPTION'
TRIAG = 'TRIAGE'
TRIAG_U = 'TRIAGE_URGENT'
WAI_N = 'WAIT_NO_URGENT'
WAI_U = 'WAIT_URGENT'
N_URG = 'NOT_URGENT'
U_URG = 'URGENT'
IMAGI = 'IMAGING'
LABOR = 'LABORATORY'
EXIT_ = 'EXIT'
AT_UR = 'ATTEN_URGE'
At_NU = 'ATTE_N_URG'
ARE_test = 'ARE_test'


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

"""----------------------------------------------------------------------------
                             COUNTING HCW 1
"""
def workers_count_shift_1(Users, day, count): 

    RECEP_from_shift_1 = count[0]
    TRIAG_from_shift_1 = count[1]
    # TRIAG_U_from_shift_1 = count[2]
    # N_URG_from_shift_1 = count[3]
    N_N_URG_from_shift_1 = count[2]
    # DR_URGE_from_shift_1 = count[5]
    DR_N_URG_from_shift_1= count[3]
    IMAGI_from_shift_1=  count[4]
    LABOR_from_shift_1= count[5]
    # ARE_test_from_shift_1 = count[9]
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff1_RECEPTION') ):
            cont_day = cont_day + 1
    RECEP_from_shift_1.append([day,cont_day])    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff1_TRIAGE') ):
            cont_day = cont_day + 1
    TRIAG_from_shift_1.append([day,cont_day])   
    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff1_ATTEN_URGE') ):
            cont_day = cont_day + 1
    N_N_URG_from_shift_1.append([day,cont_day])
    

    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff1_ATTE_N_URG') ):
            cont_day = cont_day + 1
    DR_N_URG_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff1_IMAGING') ):
            cont_day = cont_day + 1
    IMAGI_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff1_LABORATORY') ):
            cont_day = cont_day + 1
    LABOR_from_shift_1.append([day,cont_day])
    

    
    count= [RECEP_from_shift_1, TRIAG_from_shift_1, N_N_URG_from_shift_1,
            DR_N_URG_from_shift_1, IMAGI_from_shift_1, LABOR_from_shift_1]
    
    return count

"""----------------------------------------------------------------------------
                             COUNTING HCW 2
"""
def workers_count_shift_2(Users, day, count):
    RECEP_from_shift_2 = count[0]
    TRIAG_from_shift_2 = count[1]
    # TRIAG_U_from_shift_2 = count[2]
    # N_URG_from_shift_2 = count[3]
    N_N_URG_from_shift_2 = count[2]
    # DR_URGE_from_shift_2 = count[5]
    DR_N_URG_from_shift_2= count[3]
    IMAGI_from_shift_2=  count[4]
    LABOR_from_shift_2= count[5]
    # ARE_test_from_shift_2 = count[9]
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff2_RECEPTION') ):
            cont_day = cont_day + 1
    RECEP_from_shift_2.append([day,cont_day])    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff2_TRIAGE') ):
            cont_day = cont_day + 1
    TRIAG_from_shift_2.append([day,cont_day])   
    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff2_ATTEN_URGE') ):
            cont_day = cont_day + 1
    N_N_URG_from_shift_2.append([day,cont_day])

    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff2_ATTE_N_URG')):
            cont_day = cont_day + 1
    DR_N_URG_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff2_IMAGING') ):
            cont_day = cont_day + 1
    IMAGI_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff2_LABORATORY') ):
            cont_day = cont_day + 1
    LABOR_from_shift_2.append([day,cont_day])
    
    count= [RECEP_from_shift_2, TRIAG_from_shift_2, N_N_URG_from_shift_2,
            DR_N_URG_from_shift_2, IMAGI_from_shift_2, LABOR_from_shift_2]
    
    return count

"""----------------------------------------------------------------------------
                             COUNTING HCW 3
"""
def workers_count_shift_3(Users, day, count):
    RECEP_from_shift_3 = count[0]
    TRIAG_from_shift_3 = count[1]
    # TRIAG_U_from_shift_3 = count[2]
    # N_URG_from_shift_3 = count[3]
    N_N_URG_from_shift_3 = count[2]
    # DR_URGE_from_shift_3 = count[5]
    DR_N_URG_from_shift_3= count[3]
    IMAGI_from_shift_3=  count[4]
    LABOR_from_shift_3= count[5]
    # ARE_test_from_shift_3 = count[9]
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == "Staff3_RECEPTION") ):
            cont_day = cont_day + 1
    RECEP_from_shift_3.append([day,cont_day])    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff2_TRIAGE') ):
            cont_day = cont_day + 1
    TRIAG_from_shift_3.append([day,cont_day])   
    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff3_ATTEN_URGE') ):
            cont_day = cont_day + 1
    N_N_URG_from_shift_3.append([day,cont_day])
    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff3_ATTE_N_URG') ):
            cont_day = cont_day + 1
    DR_N_URG_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff3_IMAGING') ):
            cont_day = cont_day + 1
    IMAGI_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
            (Users[i][11] == 'Staff3_LABORATORY') ):
            cont_day = cont_day + 1
    LABOR_from_shift_3.append([day,cont_day])
    
    
    count= [RECEP_from_shift_3, TRIAG_from_shift_3, N_N_URG_from_shift_3, 
            DR_N_URG_from_shift_3, IMAGI_from_shift_3, LABOR_from_shift_3]
    
    return count

"""----------------------------------------------------------------------------
                      COUNTING percentage HCW 1
"""
def percent_staff_shift_1(worker_1, workers_count_1, count_from):
    cont_from_w_shift_1 = count_from
    RECEP_from_shift_1 = workers_count_1[0]
    TRIAG_from_shift_1 = workers_count_1[1]
    # TRIAG_U_from_shift_1 = workers_count_1[2]
    # N_URG_from_shift_1 = workers_count_1[3]
    N_N_URG_from_shift_1 = workers_count_1[2]
    # DR_URGE_from_shift_1 = workers_count_1[5]
    DR_N_URG_from_shift_1= workers_count_1[3]
    IMAGI_from_shift_1=  workers_count_1[4]
    LABOR_from_shift_1= workers_count_1[5]
    # ARE_test_from_shift_1 = workers_count_1[9]
    
    
    port_RECEP_from_shift_1 = worker_1[0]
    port_TRIAG_from_shift_1 = worker_1[1]
    # port_TRIAG_U_from_shift_1 = worker_1[2]
    # port_N_URG_from_shift_1 = worker_1[3]
    port_N_N_URG_from_shift_1 = worker_1[2]
    # port_DR_URGE_from_shift_1 = worker_1[5]
    port_DR_N_URG_from_shift_1= worker_1[3]
    port_IMAGI_from_shift_1=  worker_1[4]
    port_LABOR_from_shift_1= worker_1[5]
    # port_ARE_test_from_shift_1 = worker_1[9]

    

    count = 0
    for i in range(len(RECEP_from_shift_1)):
        if  RECEP_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (RECEP_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_RECEP_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_RECEP_from_shift_1.append([i,count])


    count = 0
    for i in range(len(TRIAG_from_shift_1)):
        if TRIAG_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (TRIAG_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_TRIAG_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_from_shift_1.append([i,count])
    



    count = 0
    for i in range(len(N_N_URG_from_shift_1)):
        if N_N_URG_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (N_N_URG_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_N_N_URG_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_N_N_URG_from_shift_1.append([i,count])
        

    count = 0
    for i in range(len(DR_N_URG_from_shift_1)):
        if DR_N_URG_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (DR_N_URG_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_DR_N_URG_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_N_URG_from_shift_1.append([i,count])
        

    count = 0
    for i in range(len(IMAGI_from_shift_1)):
        if IMAGI_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (IMAGI_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_IMAGI_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_IMAGI_from_shift_1.append([i,count])
        
    count = 0
    for i in range(len(LABOR_from_shift_1)):
        if LABOR_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (LABOR_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_LABOR_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_LABOR_from_shift_1.append([i,count])
        

            
    worker_1 =  [port_RECEP_from_shift_1, port_TRIAG_from_shift_1, 
                 port_N_N_URG_from_shift_1, port_DR_N_URG_from_shift_1, 
                 port_IMAGI_from_shift_1, port_LABOR_from_shift_1]
            
    
    return worker_1

"""----------------------------------------------------------------------------
                      COUNTING percentage HCW 2
"""
def percent_staff_shift_2(worker_2,workers_count_2,count_from):
    cont_from_w_shift_2 = count_from
    RECEP_from_shift_2 = workers_count_2[0]
    TRIAG_from_shift_2 = workers_count_2[1]
    # TRIAG_U_from_shift_2 = workers_count_2[2]
    # N_URG_from_shift_2 = workers_count_2[3]
    N_N_URG_from_shift_2 = workers_count_2[2]
    # DR_URGE_from_shift_2 = workers_count_2[5]
    DR_N_URG_from_shift_2= workers_count_2[3]
    IMAGI_from_shift_2=  workers_count_2[4]
    LABOR_from_shift_2= workers_count_2[5]
    # ARE_test_from_shift_2 = workers_count_2[9]
    
    port_RECEP_from_shift_2 = worker_2[0]
    port_TRIAG_from_shift_2 = worker_2[1]
    # port_TRIAG_U_from_shift_2 = worker_2[2]
    # port_N_URG_from_shift_2 = worker_2[3]
    port_N_N_URG_from_shift_2 = worker_2[2]
    # port_DR_URGE_from_shift_2 = worker_2[5]
    port_DR_N_URG_from_shift_2= worker_2[3]
    port_IMAGI_from_shift_2=  worker_2[4]
    port_LABOR_from_shift_2= worker_2[5]
    # port_ARE_test_from_shift_2 = worker_2[9]

    count = 0
    for i in range(len(RECEP_from_shift_2)):
        if RECEP_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (RECEP_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_RECEP_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_RECEP_from_shift_2.append([i,count])



    count = 0
    for i in range(len(TRIAG_from_shift_2)):
        if TRIAG_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (TRIAG_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_TRIAG_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_from_shift_2.append([i,count])


    count = 0
    for i in range(len(N_N_URG_from_shift_2)):
        if N_N_URG_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (N_N_URG_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_N_N_URG_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_N_N_URG_from_shift_2.append([i,count])



    count = 0
    for i in range(len(DR_N_URG_from_shift_2)):
        if DR_N_URG_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (DR_N_URG_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_DR_N_URG_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_N_URG_from_shift_2.append([i,count])
        

    count = 0
    for i in range(len(IMAGI_from_shift_2)):
        if IMAGI_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (IMAGI_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_IMAGI_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_IMAGI_from_shift_2.append([i,count])
        


    count = 0
    for i in range(len(LABOR_from_shift_2)):
        if LABOR_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (LABOR_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_LABOR_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_LABOR_from_shift_2.append([i,count])
        

            
    worker_2 =  [port_RECEP_from_shift_2, port_TRIAG_from_shift_2, 
                 port_N_N_URG_from_shift_2, port_DR_N_URG_from_shift_2, 
                 port_IMAGI_from_shift_2, port_LABOR_from_shift_2]
            
    
    return worker_2

"""----------------------------------------------------------------------------
                      COUNTING percentage HCW 3
"""
def percent_staff_shift_3(worker_3,workers_count_3,count_from):
    cont_from_w_shift_3 = count_from
    RECEP_from_shift_3 = workers_count_3[0]
    TRIAG_from_shift_3 = workers_count_3[1]
    # TRIAG_U_from_shift_3 = workers_count_3[2]
    # N_URG_from_shift_3 = workers_count_3[3]
    N_N_URG_from_shift_3 = workers_count_3[2]
    # DR_URGE_from_shift_3 = workers_count_3[5]
    DR_N_URG_from_shift_3= workers_count_3[3]
    IMAGI_from_shift_3=  workers_count_3[4]
    LABOR_from_shift_3= workers_count_3[5]
    # ARE_test_from_shift_3 = workers_count_3[9]
    
    port_RECEP_from_shift_3 = worker_3[0]
    port_TRIAG_from_shift_3 = worker_3[1]
    # port_TRIAG_U_from_shift_3 = worker_3[2]
    # port_N_URG_from_shift_3 = worker_3[3]
    port_N_N_URG_from_shift_3 = worker_3[2]
    # port_DR_URGE_from_shift_3 = worker_3[5]
    port_DR_N_URG_from_shift_3= worker_3[3]
    port_IMAGI_from_shift_3=  worker_3[4]
    port_LABOR_from_shift_3= worker_3[5]
    # port_ARE_test_from_shift_3 = worker_3[9]


    count = 0
    for i in range(len(RECEP_from_shift_3)):
        if RECEP_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (RECEP_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_RECEP_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_RECEP_from_shift_3.append([i,count])

    count = 0
    for i in range(len(TRIAG_from_shift_3)):
        if TRIAG_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (TRIAG_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_TRIAG_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_from_shift_3.append([i,count])


    count = 0
    for i in range(len(N_N_URG_from_shift_3)):
        if N_N_URG_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (N_N_URG_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_N_N_URG_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_N_N_URG_from_shift_3.append([i,count])
        


    count = 0
    for i in range(len(DR_N_URG_from_shift_3)):
        if DR_N_URG_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (DR_N_URG_from_shift_3[i][1]*100)/cont_from_w_shift_3[i][1]
            port_DR_N_URG_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_N_URG_from_shift_3.append([i,count])

    count = 0
    for i in range(len(IMAGI_from_shift_3)):
        if IMAGI_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (IMAGI_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_IMAGI_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_IMAGI_from_shift_3.append([i,count])
        


    count = 0
    for i in range(len(LABOR_from_shift_3)):
        if LABOR_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (LABOR_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_LABOR_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_LABOR_from_shift_3.append([i,count])
        
        


            
    worker_3 =  [port_RECEP_from_shift_3, port_TRIAG_from_shift_3, 
                 port_N_N_URG_from_shift_3, port_DR_N_URG_from_shift_3, 
                 port_IMAGI_from_shift_3, port_LABOR_from_shift_3]
            
    
    return worker_3


def proport_user_day(day,Users,User_propo_num):
    
    Recep_port = User_propo_num[0]
    Triag_port = User_propo_num[1]
    WaitU_port = User_propo_num[2]
    WaitN_port = User_propo_num[3]
    AtteU_port = User_propo_num[4]
    AtteN_port = User_propo_num[5]
    Imagi_port = User_propo_num[6]
    Labot_port = User_propo_num[7]
    
    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if ( (Users[i][11] == PATIEN+'_RECEPTION') or 
              (Users[i][11] == 'Staff1_RECEPTION') or 
              (Users[i][11] == 'Staff2_RECEPTION') or 
              (Users[i][11] == 'Staff3_RECEPTION') ) :
                if (Users[i][11] == PATIEN+'_RECEPTION'):
                    pati = pati + 1
                if ((Users[i][11] == 'Staff1_RECEPTION') or 
                    (Users[i][11] == 'Staff2_RECEPTION') or 
                    (Users[i][11] == 'Staff3_RECEPTION') ):
                    HCW = HCW + 1
    Recep_port.append([pati,HCW])
    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if ( (Users[i][11] == PATIEN+'_TRIAGE') or 
              (Users[i][11] == 'Staff1_TRIAGE') or 
              (Users[i][11] == 'Staff2_TRIAGE') or 
              (Users[i][11] == 'Staff3_TRIAGE') ) :
                if (Users[i][11] == PATIEN+'_TRIAGE'):
                    pati = pati + 1
                if ((Users[i][11] == 'Staff1_TRIAGE') or 
                    (Users[i][11] == 'Staff2_TRIAGE') or 
                    (Users[i][11] == 'Staff3_TRIAGE') ):
                    HCW = HCW + 1
    Triag_port.append([pati,HCW])
    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if (Users[i][11] =='WAIT_URGENT') :
                if (Users[i][11] == 'WAIT_URGENT'):
                    pati = pati + 1
    WaitU_port.append([pati,HCW])
    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if (Users[i][11] =='WAIT_NO_URGENT') :
                if (Users[i][11] == 'WAIT_NO_URGENT'):
                    pati = pati + 1
    WaitN_port.append([pati,HCW])

    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if ( (Users[i][11] == PATIEN+'_ATTEN_URGE') or 
              (Users[i][11] == 'Staff1_ATTEN_URGE') or 
              (Users[i][11] == 'Staff2_ATTEN_URGE') or 
              (Users[i][11] == 'Staff3_ATTEN_URGE') ) :
                if (Users[i][11] == PATIEN+'_ATTEN_URGE'):
                    pati = pati + 1
                if ((Users[i][11] == 'Staff1_ATTEN_URGE') or 
                    (Users[i][11] == 'Staff2_ATTEN_URGE') or 
                    (Users[i][11] == 'Staff3_ATTEN_URGE') ):
                    HCW = HCW + 1
    AtteU_port.append([pati,HCW])
    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if ( (Users[i][11] == PATIEN +'_ATTE_N_URG') or 
              (Users[i][11] == 'Staff1_ATTE_N_URG') or 
              (Users[i][11] == 'Staff2_ATTE_N_URG') or 
              (Users[i][11] == 'Staff3_ATTE_N_URG') ) :
                if (Users[i][11] == PATIEN +'_ATTE_N_URG'):
                    pati = pati + 1
                if ((Users[i][11] == 'Staff1_ATTE_N_URG') or 
                    (Users[i][11] == 'Staff2_ATTE_N_URG') or 
                    (Users[i][11] == 'Staff3_ATTE_N_URG') ):
                    HCW = HCW + 1
    AtteN_port.append([pati,HCW])
    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if ( (Users[i][11] == PATIEN +'_IMAGING') or 
              (Users[i][11] == 'Staff1_IMAGING') or 
              (Users[i][11] == 'Staff2_IMAGING') or 
              (Users[i][11] == 'Staff3_IMAGING') ) :
                if (Users[i][11] == PATIEN +'_IMAGING'):
                    pati = pati + 1
                if ((Users[i][11] == 'Staff1_IMAGING') or 
                    (Users[i][11] == 'Staff2_IMAGING') or 
                    (Users[i][11] == 'Staff3_IMAGING') ):
                    HCW = HCW + 1
    Imagi_port.append([pati,HCW])
    
    
    pati = 0
    HCW = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) ): 
            if ( (Users[i][11] == PATIEN +'_LABORATORY') or 
              (Users[i][11] == 'Staff1_LABORATORY') or 
              (Users[i][11] == 'Staff2_LABORATORY') or 
              (Users[i][11] == 'Staff3_LABORATORY') ) :
                if (Users[i][11] == PATIEN +'_LABORATORY'):
                    pati = pati + 1
                if ((Users[i][11] == 'Staff1_LABORATORY') or 
                    (Users[i][11] == 'Staff2_LABORATORY') or 
                    (Users[i][11] == 'Staff3_LABORATORY') ):
                    HCW = HCW + 1
    Labot_port.append([pati,HCW])
    
            
            

    
    User_propo_num = [Recep_port,
                            Triag_port,
                            WaitU_port,
                            WaitN_port,
                            AtteU_port,
                            AtteN_port,
                            Imagi_port,
                            Labot_port]
    
    return User_propo_num




def proportion_user_tot(User_propot,propo_area,Total_patien_inf):
      
    Recep_propo = propo_area[0]
    Triag_propo = propo_area[1]
    WaitU_propo = propo_area[2]
    WaitN_propo = propo_area[3]
    AtteU_propo = propo_area[4]
    AtteN_propo = propo_area[5]
    Imagi_propo = propo_area[6]
    Labot_propo = propo_area[7]
    
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[0])):
        Tot_pat = Tot_pat + User_propot[0][k][0]
        Tot_HCW = Tot_HCW + User_propot[0][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    Recep_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[1])):
        Tot_pat = Tot_pat + User_propot[1][k][0]
        Tot_HCW = Tot_HCW + User_propot[1][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    Triag_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[2])):
        Tot_pat = Tot_pat + User_propot[2][k][0]
        Tot_HCW = Tot_HCW + User_propot[2][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    WaitU_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[3])):
        Tot_pat = Tot_pat + User_propot[3][k][0]
        Tot_HCW = Tot_HCW + User_propot[3][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    WaitN_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[4])):
        Tot_pat = Tot_pat + User_propot[4][k][0]
        Tot_HCW = Tot_HCW + User_propot[4][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    AtteU_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[5])):
        Tot_pat = Tot_pat + User_propot[5][k][0]
        Tot_HCW = Tot_HCW + User_propot[5][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    AtteN_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[6])):
        Tot_pat = Tot_pat + User_propot[6][k][0]
        Tot_HCW = Tot_HCW + User_propot[6][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    Imagi_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(User_propot[7])):
        Tot_pat = Tot_pat + User_propot[7][k][0]
        Tot_HCW = Tot_HCW + User_propot[7][k][1]
    if Total_patien_inf == 0:
        por_pat = 0
        por_hcw = 0
    else:
        por_pat =  (Tot_pat*100)/Total_patien_inf
        por_hcw = (Tot_HCW*100)/Total_patien_inf
    Labot_propo = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    propo_area = [Recep_propo,Triag_propo,WaitU_propo,WaitN_propo,
                   AtteU_propo,AtteN_propo,Imagi_propo,Labot_propo]
    
    return propo_area



def proport_HCW_day(day,Users_workers_shift_1,Users_workers_shift_2,
                    Users_workers_shift_3,HCW_propo_num):
    
    Recep_port_HCW = HCW_propo_num[0]
    Triag_port_HCW = HCW_propo_num[1]
    AtteU_port_HCW = HCW_propo_num[2]
    AtteN_port_HCW = HCW_propo_num[3]
    Imagi_port_HCW = HCW_propo_num[4]
    Labot_port_HCW = HCW_propo_num[5]
    Base1_port_HCW = HCW_propo_num[6]
    Base2_port_HCW = HCW_propo_num[7]
    Base3_port_HCW = HCW_propo_num[8]
    
    HCW_list = []
    HCW_list.append(Users_workers_shift_1)
    HCW_list.append(Users_workers_shift_2)
    HCW_list.append(Users_workers_shift_3)
    
    
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                if HCW_list[i][k][5] == PATIEN+'_RECEPTION':
                    pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff1_RECEPTION') or
                    (HCW_list[i][k][5] == 'Staff2_RECEPTION') or 
                    (HCW_list[i][k][5] == 'Staff3_RECEPTION') ):
                    HCW = HCW + 1
    Recep_port_HCW.append([pati,HCW])
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                if HCW_list[i][k][5] == PATIEN+'_TRIAGE':
                    pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff1_TRIAGE') or
                    (HCW_list[i][k][5] == 'Staff2_TRIAGE') or 
                    (HCW_list[i][k][5] == 'Staff3_TRIAGE') ):
                    HCW = HCW + 1
    Triag_port_HCW.append([pati,HCW])
    
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                if HCW_list[i][k][5] == 'PATIENT_ATTEN_URGE':
                    pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff1_ATTEN_URGE') or
                    (HCW_list[i][k][5] == 'Staff2_ATTEN_URGE') or 
                    (HCW_list[i][k][5] == 'Staff3_ATTEN_URGE') ):
                    HCW = HCW + 1
    AtteU_port_HCW.append([pati,HCW])    
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                if HCW_list[i][k][5] == 'PATIENT_ATTE_N_URG':
                    pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff1_ATTE_N_URG') or
                    (HCW_list[i][k][5] == 'Staff2_ATTE_N_URG') or 
                    (HCW_list[i][k][5] == 'Staff3_ATTE_N_URG') ):
                    HCW = HCW + 1
    AtteN_port_HCW.append([pati,HCW])
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                if HCW_list[i][k][5] == PATIEN +'_IMAGING':
                    pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff1_IMAGING') or
                    (HCW_list[i][k][5] == 'Staff2_IMAGING') or 
                    (HCW_list[i][k][5] == 'Staff3_IMAGING') ):
                    HCW = HCW + 1
    Imagi_port_HCW.append([pati,HCW])
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                if HCW_list[i][k][5] == PATIEN +'_LABORATORY':
                    pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff1_LABORATORY') or
                    (HCW_list[i][k][5] == 'Staff2_LABORATORY') or 
                    (HCW_list[i][k][5] == 'Staff3_LABORATORY') ):
                    HCW = HCW + 1
    Labot_port_HCW.append([pati,HCW])
        
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                # if HCW_list[i][k][5] == PATIEN+'_RECEPTION':
                #     pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff1_HCW_BASE') ):
                    # or
                    # (HCW_list[i][k][5] == 'Staff2_HCW_BASE') ):
                    HCW = HCW + 1
    Base1_port_HCW.append([pati,HCW])
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                # if HCW_list[i][k][5] == PATIEN+'_RECEPTION':
                #     pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff2_HCW_BASE') ):
                    # or
                    # (HCW_list[i][k][5] == 'Staff2_HCW_BASE') ):
                    HCW = HCW + 1
    Base2_port_HCW.append([pati,HCW])
    
    pati = 0
    HCW = 0
    for i in range(len(HCW_list)):
        for k in range (len(HCW_list[i])):
            if HCW_list[i][k][6] == (day + 1):
                # if HCW_list[i][k][5] == PATIEN+'_RECEPTION':
                #     pati = pati + 1
                if ((HCW_list[i][k][5] == 'Staff3_HCW_BASE')  ):
                    # or
                    # (HCW_list[i][k][5] == 'Staff1_HCW_BASE') ):
                    HCW = HCW + 1
    Base3_port_HCW.append([pati,HCW])

    
    
    User_propo_num = [Recep_port_HCW,
                        Triag_port_HCW,
                        AtteU_port_HCW,
                        AtteN_port_HCW,
                        Imagi_port_HCW,
                        Labot_port_HCW,
                        Base1_port_HCW,
                        Base2_port_HCW,
                        Base3_port_HCW]
    
    return User_propo_num



def propor_HCW_tot(HCW_propo, propo_HCW, Total_HCW_inf):

    Recep_prop_H = propo_HCW[0]
    Triag_prop_H = propo_HCW[1]
    AtteU_prop_H = propo_HCW[2]
    AtteN_prop_H = propo_HCW[3]
    Imagi_prop_H = propo_HCW[4]
    Labot_prop_H = propo_HCW[5]
    Base1_prop_H = propo_HCW[6]
    Base2_prop_H = propo_HCW[7]
    Base3_prop_H = propo_HCW[8]
    
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[0])):
        Tot_pat = Tot_pat + HCW_propo[0][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[0][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    Recep_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[1])):
        Tot_pat = Tot_pat + HCW_propo[1][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[1][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    Triag_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[2])):
        Tot_pat = Tot_pat + HCW_propo[2][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[2][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    AtteU_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[3])):
        Tot_pat = Tot_pat + HCW_propo[3][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[3][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    AtteN_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[4])):
        Tot_pat = Tot_pat + HCW_propo[4][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[4][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    Imagi_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[5])):
        Tot_pat = Tot_pat + HCW_propo[5][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[5][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    Labot_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[6])):
        Tot_pat = Tot_pat + HCW_propo[6][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[6][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    Base1_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[7])):
        Tot_pat = Tot_pat + HCW_propo[7][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[7][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    Base2_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    Tot_pat = 0
    Tot_HCW = 0
    for k in range(len(HCW_propo[8])):
        Tot_pat = Tot_pat + HCW_propo[8][k][0]
        Tot_HCW = Tot_HCW + HCW_propo[8][k][1]
    if Total_HCW_inf == 0:
        por_pat = 0
        por_hcw = 0
    else: 
        por_pat =  (Tot_pat*100)/Total_HCW_inf
        por_hcw = (Tot_HCW*100)/Total_HCW_inf
    Base3_prop_H = [por_pat,por_hcw,Tot_pat,Tot_HCW]
    
    
    propo_HCW = [Recep_prop_H,Triag_prop_H, AtteU_prop_H,AtteN_prop_H,
                  Imagi_prop_H,Labot_prop_H,Base1_prop_H,Base2_prop_H,
                  Base3_prop_H]
    
    return propo_HCW



def average_funct(save_results, save_PAT, save_HCW):
    
    
    # Recep_P = []
    # Triag_P = []
    # WaitU_P = []
    # WaitN_P = []
    # AtteU_P = []
    # AtteN_P = []
    # Imagi_P = []
    # Labot_P = []
    
    # Recep_prop_H = []
    # Triag_prop_H = []
    # AtteU_prop_H = []
    # AtteN_prop_H = []
    # Imagi_prop_H = []
    # Labot_prop_H = []
    # Base1_prop_H = []
    # Base2_prop_H = []
    # Base3_prop_H = []

    
    # suma_P = 0
    # suma_H  = 0
    # for i in len(save_results):
    #     Recep_P.append(save_results[i][0][0])
    #     Triag_P.append(save_results[i][0][1])
    #     WaitU_P.append(save_results[i][0][2])
    #     WaitN_P.append(save_results[i][0][3])
    #     AtteU_P.append(save_results[i][0][4])
    #     AtteN_P.append(save_results[i][0][5])
    #     Imagi_P.append(save_results[i][0][6])
    #     Labot_P.append(save_results[i][0][7])
        
    #     Recep_prop_H.append(save_results[i][1][0])
    #     Triag_prop_H.append(save_results[i][1][1])
    #     AtteU_prop_H.append(save_results[i][1][2])
    #     AtteN_prop_H.append(save_results[i][1][3])
    #     Imagi_prop_H.append(save_results[i][1][4])
    #     Labot_prop_H.append(save_results[i][1][5])
    #     Base1_prop_H.append(save_results[i][1][6])
    #     Base2_prop_H.append(save_results[i][1][7])
    #     Base3_prop_H.append(save_results[i][1][8])
        
        
        
        
    # a = [2, 5, 1, 9]
    # b = [4, 9, 5, 10]
    
    # result = [statistics.mean(k) for k in zip(a, b)]
    # # -> [3.0, 7.0, 3.0, 9.5]
    
    return save_results











