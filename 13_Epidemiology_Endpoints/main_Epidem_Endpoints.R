
#' -----------------------------------------------------------------------------
#' 
#'                         Epidemiology Endpoints
#' 
#' Architectural interventions to mitigate the spread of
#' SARS-CoV-2 in emergency departments
#' 
#' InnoBRI project 
#' This work was supported by the Innovation Funds of the 
#' Joint Federal Committee 
#' (Innovationsfonds des gemeinsamen Bundesausschusses (G-BA),
#'   funding reference: 01VSF19032)
#' 
#' NOTES: This file runs the Epidemiology Endpoints.
#'
#' We calculate the incidence rate ratio (IRR) and the incidence rate difference
#' (IRD) per 1,000 person-months for various infection-related endpoints and 
#' compared to the base case in a typical ED in Germany.
#' Endpoints: Infections | Hospitalizations | ICU admissions | Deaths
#' 
#'  ----------------------------------------------------------------------------



#% ----       If needed for packages installation
# % install.packages("readxl") 
# % install.packages("data.table")
# % install.packages("writexl")
# % install.packages("tidyverse")

rm(list = ls())
library(readxl)
library(dplyr)
library(tidyverse)
library(writexl)
library(parallel)
library(data.table)



#-----------        Path for reading data from simulation
# path <- "C:/Users/mejia/Downloads/1_Epi_test/1_Simulation_Results/"
path <- "C:/Users/.../1_Simulation_Results"

#-----------      Path for saving Epi endpoint resutls

# path_save <- "C:/Users/mejia/Downloads/1_Epi_test/2_Epidem_Endpoints/"
path_save <- "C:/Users/.../2_Epidem_Endpoints"


#----------------      AGE DISTRIBUTIONS ED PATIENTS    ------------------------
#Age distribution of ED non-surgical patients (only adults) from 
#Table 4 - M. Michael et al., "Age- and gender-associated distribution 
# of type of admission, triage, type of discharge, and length of stay in the 
# emergency department," Notfall und Rettungsmedizin, pp. 1-10, May 2021.

Pat_greater90 <- 2.81 / 100
Pat_80_89 <- 13.3 / 100
Pat_70_79 <- 14.55 / 100
Pat_60_69 <- 13.68 / 100
Pat_50_59 <- 14.15 / 100
Pat_40_49 <- 12.13 / 100
Pat_30_39 <- 13.08 / 100
Pat_18_29 <- 16.3 / 100

#-------------------------------------------------------------------------------


#----------------       AGE DISTRIBUTIONS ED HCWs      - -----------------------
# assume uniform distribution between age 18 and 65
HCW_18_29 <- (29-18+1) * 1/48
HCW_30_39 <- (39-30+1) * 1/48
HCW_40_49 <- (49-40+1) * 1/48
HCW_50_59 <- (59-50+1) * 1/48
HCW_60_65 <- (65-60+1) * 1/48

#-------------------------------------------------------------------------------


#----------------       PROP SYMP/HOSP/ICU/INT/MORT     ------------------------

# Proportion of all positive cases which remain asymptomatic within age groups
# P. Sah et al., "Asymptomatic SARS-CoV-2 infection: A systematic 
# review and meta-analysis," Proc. Natl. Acad. Sci. U. S. A., vol. 118, no. 34, 
# Aug. 2021.

Asymp_19_59 <- 32.1 / 100
Asymp_greater60 <- 19.7 / 100
# from above
all_symp_19_59 <- 1-Asymp_19_59
all_symp_greater60 <- 1-Asymp_greater60


# Proportions of patients needing the hospital among detected patients 
# within each age group -> LZG data/IfSG
Det_hosp_18_59 <- 6 / 100
Det_hosp_60_69 <- 18.8 / 100
Det_hosp_70_79 <- 37 / 100
Det_hosp_greater80 <- 47.3 / 100


# Proportion of patients needing the ICU among hospitalised patients
# ASSUMPTION = 25% of hospitalised patients as assumed for LZG/Krisenstab Model
hosp_icu_allage <- 0.25


# Proportions of patients needing intubation among hospitalised patients 
# C. Karagiannidis et al., "Case characteristics, resource use, and 
# outcomes of 10021 patients with COVID-19 admitted to 920 German hospitals: 
# an observational study," Lancet Respir. Med., vol. 8, no. 9, Sep. 2020.
Hosp_int_18_59 <- 14.6 / 100
Hosp_int_60_69 <- 23.6 / 100
Hosp_int_70_79 <- 24.8 / 100
Hosp_int_greater80 <- 11.6 / 100


# Proportions of dead patients among detected patients within each age group
# J. Schilling et al., "Krankheitsschwere der ersten COVID-19-Welle 
# in Deutschland basierend auf den Meldungen gemäß Infektionsschutzgesetz," 
# J. Heal. Monit., 2020.
Det_mort_20_39 <- 0.1 / 100
Det_mort_40_59 <- 0.7 / 100
Det_mort_60_79 <- 9.6 / 100  
Det_mort_greater80 <- 30 / 100

# Mort of all infectious 
Inf_mort_20_39 <- Det_mort_20_39*0.25
Inf_mort_40_59 <- Det_mort_40_59*0.25
Inf_mort_60_79 <- Det_mort_60_79*0.25
Inf_mort_greater80 <-Det_mort_greater80*0.25

#-------------------------------------------------------------------------------



#------------   WEIGHTED PROPORTIONS SYMP/HOSP/ICU/INT/MORT  -------------------
#Proportion symptomatic from all infected
(Pat_symp_agecombined <- ((Pat_18_29+Pat_30_39+Pat_40_49+Pat_50_59)*
                            all_symp_19_59 + (Pat_60_69+Pat_70_79+Pat_80_89+
                                            Pat_greater90)*all_symp_greater60))
(HCW_symp_agecombined <- (HCW_18_29+HCW_30_39+HCW_40_49+HCW_50_59)*
                                 all_symp_19_59 + HCW_60_65*all_symp_greater60)

# Proportion hospitalised from all detected.  
(Pat_det_hosp_agecombined <- 
    (Pat_18_29+Pat_30_39+Pat_40_49+Pat_50_59)*Det_hosp_18_59 + 
    Pat_60_69*Det_hosp_60_69 + 
    Pat_70_79*Det_hosp_70_79 + 
    (Pat_80_89+Pat_greater90)*Det_hosp_greater80)

(HCW_det_hosp_agecombined <- 
    (HCW_18_29+HCW_30_39+HCW_40_49+HCW_50_59)*Det_hosp_18_59 + 
    HCW_60_65*Det_hosp_60_69)


#  Proportion ICU from all hospitalised
(Pat_det_icu_agecombined <- 
    (Pat_18_29+Pat_30_39+Pat_40_49+Pat_50_59)*Det_hosp_18_59*hosp_icu_allage + 
    Pat_60_69*Det_hosp_60_69*hosp_icu_allage + 
    Pat_70_79*Det_hosp_70_79*hosp_icu_allage + 
    (Pat_80_89+Pat_greater90)*Det_hosp_greater80*hosp_icu_allage)

(HCW_det_icu_agecombined <- 
    (HCW_18_29+HCW_30_39+HCW_40_49+HCW_50_59)*Det_hosp_18_59*hosp_icu_allage + 
    HCW_60_65*Det_hosp_60_69*hosp_icu_allage)

# Proportion Intubated from all hospitalised
(Pat_det_int_agecombined <- 
    (Pat_18_29+Pat_30_39+Pat_40_49+Pat_50_59)*Det_hosp_18_59*Hosp_int_18_59 + 
    Pat_60_69*Det_hosp_60_69*Hosp_int_60_69 + 
    Pat_70_79*Det_hosp_70_79*Hosp_int_70_79 + 
    (Pat_80_89+Pat_greater90)*Det_hosp_greater80*Hosp_int_greater80)

(HCW_det_int_agecombined <- 
    (HCW_18_29+HCW_30_39+HCW_40_49+HCW_50_59)*Det_hosp_18_59*Hosp_int_18_59 + 
    HCW_60_65*Det_hosp_60_69*Hosp_int_60_69)


# Proportion dead from all detected
(Pat_det_mort_agecombined <- 
    (Pat_18_29 + Pat_30_39)*Det_mort_20_39 +
    (Pat_40_49 + Pat_50_59)*Det_mort_40_59 +
    (Pat_60_69 + Pat_70_79)*Det_mort_60_79 +
    (Pat_80_89 + Pat_greater90)*Det_mort_greater80)

(HCW_det_mort_agecombined <- 
    (HCW_18_29+HCW_30_39)*Det_mort_20_39 +
    (HCW_40_49+HCW_50_59+HCW_60_65)*Det_mort_40_59)


#  Proportion hospitalised from all infected. 
#  ASSUMPTION 25% of cases detected
Pat_hosp_agecombined <- Pat_det_hosp_agecombined*0.25
HCW_hosp_agecombined <- HCW_det_hosp_agecombined*0.25
#Proportion ICU from all infected. 
Pat_icu_agecombined <- Pat_det_icu_agecombined*0.25
HCW_icu_agecombined <- HCW_det_icu_agecombined*0.25
#Proportion intubated from all infected. 
Pat_int_agecombined <- Pat_det_int_agecombined*0.25
HCW_int_agecombined <- HCW_det_int_agecombined*0.25
#Proportion dead from all infected. 
Pat_mort_agecombined <- Pat_det_mort_agecombined*0.25
HCW_mort_agecombined <- HCW_det_mort_agecombined*0.25
#-------------------------------------------------------------------------------



#-----------------------           SCENARIOS           -------------------------

#    1 - Base Case
#    2. Flexible Partitions (FP)
#          (in the code, the intervention can be found as "curtains")
#    3. Attention Area Separation (AS)
#    4. Holding Area Separation (HS)
#          (in the code, the intervention can be found as "waiting separation")
#    5. ED Base Separation (EBS)
#          (in the code, ED Base can be found as "Nurse base")
#    6. ED Base Extension (EBE)
#    7. Ventilation (Vent)
#    8. HS + AS
#    9. FP + Vent
#    10. AS + Vent
#    11. EBE + Vent
#    12. AS + EBE + Vent

#-----------------------

#                                1. Base case
Pat0 <- read_excel(paste0(path, "1_Base_case/Base_Total_Pat.xlsx"))
Pat0 <- Pat0 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P0=Total_inf_P)
HCW0 <- read_excel(paste0(path, "1_Base_case/Base_Total_HCW.xlsx"))
HCW0 <- HCW0 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H0=Total_inf_H)

#                       2. Flexible Partitions (FP)
Pat2 <- read_excel(paste0(path, "2_CURTAINS_ATTEN_AREAS/Base_Total_Pat.xlsx"))
Pat2 <- Pat2 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P2=Total_inf_P)
HCW2 <- read_excel(paste0(path, "2_CURTAINS_ATTEN_AREAS/Base_Total_HCW.xlsx"))
HCW2 <- HCW2 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H2=Total_inf_H)

#                      3. Attention Area Separation (AS)
Pat6 <- read_excel(paste0(path, (
                    "6_ATTEN_NU_DIV_AD_plus_Curt_Ventil/Base_Total_Pat.xlsx")))
Pat6 <- Pat6 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P6=Total_inf_P)
HCW6 <- read_excel(paste0(path, 
                    "6_ATTEN_NU_DIV_AD_plus_Curt_Ventil/Base_Total_HCW.xlsx"))
HCW6 <- HCW6 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H6=Total_inf_H)


#                      4. Holding Area Separation (HS)
Pat5 <- read_excel(paste0(path, 
                     "5_WAIT_NU_DIV_WD_plus_Curt_Ventil/Base_Total_Pat.xlsx"))
Pat5 <- Pat5 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P5=Total_inf_P)
HCW5 <- read_excel(paste0(path, 
                      "5_WAIT_NU_DIV_WD_plus_Curt_Ventil/Base_Total_HCW.xlsx"))
HCW5 <- HCW5 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H5=Total_inf_H)


#                          5. ED Base Separation (EBS)
Pat8 <- read_excel(paste0(path, "8_NB_sppit_plus_all/Base_Total_Pat.xlsx"))
Pat8 <- Pat8 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P8=Total_inf_P)
HCW8 <- read_excel(paste0(path, "8_NB_sppit_plus_all/Base_Total_HCW.xlsx"))
HCW8 <- HCW8 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H8=Total_inf_H)

#                          6. ED Base Extension (EBE)
Pat9 <- read_excel(paste0(path, "9_NB_volm_plus_all/Base_Total_Pat.xlsx"))
Pat9 <- Pat9 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P9=Total_inf_P)
HCW9 <- read_excel(paste0(path, "9_NB_volm_plus_all/Base_Total_HCW.xlsx"))
HCW9 <- HCW9 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H9=Total_inf_H)

#                           7. Ventilation (Vent)
Pat3 <- read_excel(paste0(path, "3_VENTILATION_ED/Base_Total_Pat.xlsx"))
Pat3 <- Pat3 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P3=Total_inf_P)
HCW3 <- read_excel(paste0(path, "3_VENTILATION_ED/Base_Total_HCW.xlsx"))
HCW3 <- HCW3 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H3=Total_inf_H)

#                                 8. HS + AS
Pat7 <- read_excel(paste0(path, "7_WD_AD_Curt_Ventil/Base_Total_Pat.xlsx"))
Pat7 <- Pat7 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P7=Total_inf_P)
HCW7 <- read_excel(paste0(path, "7_WD_AD_Curt_Ventil/Base_Total_HCW.xlsx"))
HCW7 <- HCW7 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                      Total_inf_H7=Total_inf_H)

#                               9. FP + Vent
Pat4 <- read_excel(paste0(path, "4_CURT_VENTIL/Base_Total_Pat.xlsx"))
Pat4 <- Pat4 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                      Total_inf_P4=Total_inf_P)
HCW4 <- read_excel(paste0(path, "4_CURT_VENTIL/Base_Total_HCW.xlsx"))
HCW4 <- HCW4 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                     Total_inf_H4=Total_inf_H)

#                             10. AS + Vent
Pat10 <- read_excel(paste0(path, "10_AS_Vent/Base_Total_Pat.xlsx"))
Pat10 <- Pat10 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                    Total_inf_P10=Total_inf_P)
HCW10 <- read_excel(paste0(path, "10_AS_Vent/Base_Total_HCW.xlsx"))
HCW10 <- HCW10 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                    Total_inf_H10=Total_inf_H)

#                             11. EBE + Vent
Pat11 <- read_excel(paste0(path, "11_NBV_Vent/Base_Total_Pat.xlsx"))
Pat11 <- Pat11 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                    Total_inf_P11=Total_inf_P)
HCW11 <- read_excel(paste0(path, "11_NBV_Vent/Base_Total_HCW.xlsx"))
HCW11 <- HCW11 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                    Total_inf_H11=Total_inf_H)

#                             12. AS + EBE + Vent
Pat12 <- read_excel(paste0(path, "12_AS_NBV_Vent/Base_Total_Pat.xlsx"))
Pat12 <- Pat12 %>% select("...1", "Total_inf_P") %>% rename(run=...1, 
                                                    Total_inf_P12=Total_inf_P)
HCW12 <- read_excel(paste0(path, "12_AS_NBV_Vent/Base_Total_HCW.xlsx"))
HCW12 <- HCW12 %>% select(...1, Total_inf_H) %>% rename(run=...1, 
                                                    Total_inf_H12=Total_inf_H)



#                 Combine all scenarios into one data frame

Pat_list <- list(Pat0, Pat2, Pat3, Pat4, Pat5, Pat6, Pat7,
                 Pat8, Pat9, Pat10, Pat11, Pat12)

Pat <- Pat_list %>% reduce(full_join, by="run")
HCW_list <- list(HCW0, HCW2, HCW3, HCW4, HCW5, HCW6,
                 HCW7, HCW8, HCW9, HCW10, HCW11, HCW12)
HCW <- HCW_list %>% reduce(full_join, by="run")
All <- merge(Pat, HCW, by="run")
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
#-------------        For number of Sympt, Hosp, ICU, Int, Dead      -----------
Pat_names <- c(names(Pat))
#Pat_names <- Pat_names[2:11]
Pat_names <- Pat_names[2:14]
Pat_names_2 <- c("Pat0", "Pat2", "Pat3", "Pat4", "Pat5",
                 "Pat6", "Pat7", "Pat8", "Pat9", "Pat10", "Pat11", "Pat12")
HCW_names <- c(names(HCW))
#HCW_names <- HCW_names[2:11]
HCW_names <- HCW_names[2:14]
HCW_names_2 <- c("HCW0", "HCW2", "HCW3", "HCW4", "HCW5",
                 "HCW6", "HCW7", "HCW8", "HCW9", "HCW10", "HCW11", "HCW12")
All_names_2 <- c("0", "2", "3", "4", "5",
                 "6", "7", "8", "9", "10", "11", "12")

#---------------------            Main loop
i=0
for (c in 1:12){
  i=i+1

  old_variable_Pat = eval(Pat_names[i])
  old_variable_HCW = eval(HCW_names[i])
  
  #Symp
  new_variable_Pat = eval(paste0("Symp_",Pat_names_2[i]))
  new_variable_HCW = eval(paste0("Symp_",HCW_names_2[i]))
  new_variable_all = eval(paste0("Symp_",All_names_2[i]))
  
  All <- All %>% mutate(!!as.name(new_variable_Pat) := 
                          !!as.name(old_variable_Pat)*Pat_symp_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_HCW) := 
                          !!as.name(old_variable_HCW)*HCW_symp_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_all) := 
                          !!as.name(new_variable_Pat) + 
                          !!as.name(new_variable_HCW))
  
  #Hosp
  new_variable_Pat = eval(paste0("Hosp_",Pat_names_2[i]))
  new_variable_HCW = eval(paste0("Hosp_",HCW_names_2[i]))
  new_variable_all = eval(paste0("Hosp_",All_names_2[i]))
  
  All <- All %>% mutate(!!as.name(new_variable_Pat) := 
                          !!as.name(old_variable_Pat)*Pat_hosp_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_HCW) := 
                          !!as.name(old_variable_HCW)*HCW_hosp_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_all) := 
                          !!as.name(new_variable_Pat) + 
                          !!as.name(new_variable_HCW))
  
  
  #ICU
  new_variable_Pat = eval(paste0("ICU_",Pat_names_2[i]))
  new_variable_HCW = eval(paste0("ICU_",HCW_names_2[i]))
  new_variable_all = eval(paste0("ICU_",All_names_2[i]))
  
  All <- All %>% mutate(!!as.name(new_variable_Pat) := 
                          !!as.name(old_variable_Pat)*Pat_icu_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_HCW) := 
                          !!as.name(old_variable_HCW)*HCW_icu_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_all) := 
                          !!as.name(new_variable_Pat) + 
                          !!as.name(new_variable_HCW))
  
  
  #Int
  new_variable_Pat = eval(paste0("Int_",Pat_names_2[i]))
  new_variable_HCW = eval(paste0("Int_",HCW_names_2[i]))
  new_variable_all = eval(paste0("Int_",All_names_2[i]))

  All <- All %>% mutate(!!as.name(new_variable_Pat) := 
                          !!as.name(old_variable_Pat)*Pat_int_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_HCW) := 
                          !!as.name(old_variable_HCW)*HCW_int_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_all) := 
                          !!as.name(new_variable_Pat) + 
                          !!as.name(new_variable_HCW))

  #Mortality
  new_variable_Pat = eval(paste0("Mort_",Pat_names_2[i]))
  new_variable_HCW = eval(paste0("Mort_",HCW_names_2[i]))
  new_variable_all = eval(paste0("Mort_",All_names_2[i]))
  
  All <- All %>% mutate(!!as.name(new_variable_Pat) := 
                          !!as.name(old_variable_Pat)*Pat_mort_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_HCW) := 
                          !!as.name(old_variable_HCW)*HCW_mort_agecombined)
  All <- All %>% mutate(!!as.name(new_variable_all) := 
                          !!as.name(new_variable_Pat) + 
                          !!as.name(new_variable_HCW))
  }

#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
#                              ANALYSIS PREPARATION
All <- All %>% mutate(Total_inf_0=Total_inf_P0+Total_inf_H0)
All <- All %>% mutate(Total_inf_2=Total_inf_P2+Total_inf_H2)
All <- All %>% mutate(Total_inf_3=Total_inf_P3+Total_inf_H3)
All <- All %>% mutate(Total_inf_4=Total_inf_P4+Total_inf_H4)
All <- All %>% mutate(Total_inf_5=Total_inf_P5+Total_inf_H5)
All <- All %>% mutate(Total_inf_6=Total_inf_P6+Total_inf_H6)
All <- All %>% mutate(Total_inf_7=Total_inf_P7+Total_inf_H7)
All <- All %>% mutate(Total_inf_8=Total_inf_P8+Total_inf_H8)
All <- All %>% mutate(Total_inf_9=Total_inf_P9+Total_inf_H9)
All <- All %>% mutate(Total_inf_10=Total_inf_P10+Total_inf_H10)
All <- All %>% mutate(Total_inf_11=Total_inf_P11+Total_inf_H11)
All <- All %>% mutate(Total_inf_12=Total_inf_P12+Total_inf_H12)


#  lists of names of scenarios together
infected_all_names <- c("Total_inf_0","Total_inf_2","Total_inf_3","Total_inf_4",
		"Total_inf_5","Total_inf_6","Total_inf_7","Total_inf_8","Total_inf_9",
		"Total_inf_10","Total_inf_11","Total_inf_12")
Pat_hosp_names <- paste0("Hosp_", Pat_names_2)
HCW_hosp_names <- paste0("Hosp_", HCW_names_2)
hosp_all_names <- c("Hosp_0","Hosp_2","Hosp_3","Hosp_4","Hosp_5","Hosp_6",
                    "Hosp_7","Hosp_8","Hosp_9","Hosp_10","Hosp_11","Hosp_12")
Pat_icu_names <- paste0("ICU_", Pat_names_2)
HCW_icu_names <- paste0("ICU_", HCW_names_2)
icu_all_names <- c("ICU_0","ICU_2","ICU_3","ICU_4","ICU_5","ICU_6","ICU_7",
                   "ICU_8","ICU_9","ICU_10","ICU_11","ICU_12")
Pat_mort_names <- paste0("Mort_", Pat_names_2)
HCW_mort_names <- paste0("Mort_", HCW_names_2)
mort_all_names <- c("Mort_0","Mort_2","Mort_3","Mort_4","Mort_5","Mort_6",
                    "Mort_7","Mort_8","Mort_9","Mort_10","Mort_11","Mort_12")
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#                             ANALYSIS PERFORM
#                                  INIT
# Iterations (boots trap)
number_iterations <- 100
# number of decimals rounded to, e.g. the ratio is rounded to 2 decimals 
# and the differences to 0 (as there can be no 0.12 patients)
decimals_ratio <- 2
decimals_diffs <- 2
# the differences is calculated for a typical ED (1000 Per-months), 
# for a one month period, as the original simulation time
perhowmanythousands <- 1000

#--------------------         Ratio/difference
#Function to get the ratio/difference. The name of the base_scenario needs 
# to be fed in, e.g. "Total_inf_P0" (including the "") 
#and a vector with the Names of the interventions, e.g. Pat_names

ratios_diffs <- function(base_scenario, names_of_what_to_run)
{
#             dataset to feed in results
df <- data.frame(matrix(ncol = 5, nrow = 11))
x <- c("Intervention", "Ratio","Ratio_CI", paste0("Difference_per_", 
                                                perhowmanythousands), 
                              paste0("Difference_CI_per_",perhowmanythousands))
colnames(df) <- x
# Main loop analysis
i=1
for (c in 1:11){
  i=i+1
  
  df[i-1,1] <- i-1
  
  dummy_pat_name = eval(names_of_what_to_run[i])
  
  # 
  dummy_base <- (All %>% select(run, !!as.name(base_scenario))
          %>% mutate(!!as.name(base_scenario) := !!as.name(base_scenario)/1000))
  dummy_int <- (All %>% select(run, !!as.name(dummy_pat_name)) 
        %>% mutate(!!as.name(dummy_pat_name) := !!as.name(dummy_pat_name)/1000))
  colnames(dummy_base)[2] <- "variable"
  colnames(dummy_int)[2] <- "variable"
  dummy_base$intervention <- 0
  dummy_int$intervention <- i
  dummy <- rbind(dummy_base, dummy_int)
  dummy$id <- c(1:2000)
  
  glmfit <- glm(variable ~ intervention, data = dummy, family = "poisson")
  newdata <- dummy %>% filter(intervention==i)
  p1 <- mean(predict(glmfit, newdata, type = "response"))
  newdata <- dummy %>% filter(intervention==0)
  p0 <- mean(predict(glmfit, newdata, type = "response"))
  
  df[i-1,2] <- round(p1/p0,decimals_ratio)
  df[i-1,4] <- round((p1-p0)*perhowmanythousands,decimals_diffs)
  
  bootdif <- function(dd) {
    dd <- data.table(dd)
    db <- dd[, .(run = sample(run, replace = TRUE)), keyby = intervention]
    db <- merge(db[, run, intervention], dd, by = c("run", "intervention"))
    
    glmfit <- glm(variable ~ intervention, data = db, family = "poisson")
    newdata <- db %>% filter(intervention==i)
    p1 <- mean(predict(glmfit, newdata, type = "response"))
    newdata <- db %>% filter(intervention==0)
    p0 <- mean(predict(glmfit, newdata, type = "response"))
    diff <- p1-p0
    ratio <- p1/p0
    
    return(list(diff = diff, ratio=ratio))
  }
  
  bootest <- unlist(mclapply(1:number_iterations, function(x) bootdif(dummy)))
  ratios <- bootest[seq(2,number_iterations*2+1,2)]
  diffs <- bootest[seq(1,number_iterations*2,2)]
  df[i-1,3] <- paste0("(",round(quantile(ratios, 0.025), decimals_ratio),
                  " - ", round(quantile(ratios, 0.975), decimals_ratio), ")")
  df[i-1,5] <- paste0("(",round(quantile(diffs, 0.025)*perhowmanythousands, 
                decimals_diffs), " - ", 
        round(quantile(diffs, 0.975)*perhowmanythousands, decimals_diffs), ")")

  
}
return(df)  
}

#                                  CLOSE
#                             ANALYSIS PERFORM
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
#                           RATIOS AND DIFFERENCES 
#                 Patients hospitalised, HCW needing ICU
#Infected Patients
Infected_Pat <- ratios_diffs("Total_inf_P0", Pat_names)
write_xlsx(Infected_Pat, paste0(path_save, "Infected_Patients.xlsx"))
#Infected HCW
Infected_HCW <- ratios_diffs("Total_inf_H0", HCW_names)
write_xlsx(Infected_HCW, paste0(path_save, "Infected_HCWs.xlsx"))
#Infected all
Infected_All <- ratios_diffs("Total_inf_0", infected_all_names)
write_xlsx(Infected_All, paste0(path_save, "Infected_all.xlsx"))

#Hospitalises Patients
Hospitalised_Pat <- ratios_diffs("Hosp_Pat0", Pat_hosp_names)
write_xlsx(Hospitalised_Pat, paste0(path_save, "Hospitalised_Patients.xlsx"))
#Hospitalised HCW
Hospitalised_HCW <- ratios_diffs("Hosp_HCW0", HCW_hosp_names)
write_xlsx(Hospitalised_HCW, paste0(path_save, "Hospitalised_HCWs.xlsx"))
#Hospitalised All
Hospitalised_all <- ratios_diffs("Hosp_0", hosp_all_names)
write_xlsx(Hospitalised_all, paste0(path_save, "Hospitalised_all.xlsx"))

#ICU Patients
ICU_Pat <- ratios_diffs("ICU_Pat0", Pat_icu_names)
write_xlsx(ICU_Pat, paste0(path_save, "ICU_Patients.xlsx"))
#ICU HCW
ICU_HCW <- ratios_diffs("ICU_HCW0", HCW_icu_names)
write_xlsx(ICU_HCW, paste0(path_save, "ICU_HCWs.xlsx"))
#ICU All
ICU_all <- ratios_diffs("ICU_0", icu_all_names)
write_xlsx(ICU_all, paste0(path_save, "ICU_all.xlsx"))

#Dead Patients
Mort_Pat <- ratios_diffs("Mort_Pat0", Pat_mort_names)
write_xlsx(Mort_Pat, paste0(path_save, "Mortality_Patients.xlsx"))
#Dead HCW
Mort_HCW <- ratios_diffs("Mort_HCW0", HCW_mort_names)
write_xlsx(Mort_HCW, paste0(path_save, "Mortality_HCWs.xlsx"))
#Dead All
Mort_all <- ratios_diffs("Mort_0", mort_all_names)
write_xlsx(Mort_all, paste0(path_save, "Mortality_all.xlsx"))
#-------------------------------------------------------------------------------


#--------------------------------   EOF   --------------------------------------





