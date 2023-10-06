# Architectural interventions to mitigate the spread of SARS-CoV-2 in emergency departments


## Description

In this project, we explore how architectural interventions could mitigate the spread of emerging respiratory pathogens using the example of SARS-CoV-2 during the first pandemic wave in 2020 in a prototypical emergency department (ED) setting. For more information, please refer to the paper draft.

## Dependencies

- The ED modeling platform was developed in Python 3.11
- Tool for launching parallel tasks (scenarios) - [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html#)
- Epidemiology Endpoints tests run in R


- For managing using the [command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command (default):

```
cd existing_repo
git remote add origin https://zivgitlab.uni-muenster.de/mejia/architectural_interventions_emergency_dep.git
git branch -M main
git push -uf origin main
```

## Running Scenarios
### Platform files (.py)
```main_architect_interv_ED```. This file contains the complete modeling platform for running each scenario, base case, and each architectural intervention. Comment/uncomment the code section for the scenario to be tested.

```funct_architect_interv_ED```. Contains complementary functions, callable from the main file.

```parall_architect_interv_ED```. File for launching parallel scenarios, runs X number of parallel simulations, case example with 1000 simulations. This file calls ```main_architect_interv_ED``` for running X simulations of the defined scenario at main file. Ensure changing the saving path for each new testing scenario.

```figs_architect_interv_ED```. Produce boxplots for each scenario and ED area plotting the number of new infections (patients and healthcare workers) per scenario.

### In code section for testing scenarios 

    ```
                       SCENARIOS
    
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
    ```
### Notes
Ensure the "```data_arriv```" folder path content is reachable in the main platform file "```main_architect_interv_ED```".
Ensure to **Comment/uncomment** the code section for the scenario you want to test, the case example runs the Base case (no interventions applied). 
For running the Attention Area Separation (AS), comment the base case section and uncomment the corresponding one.


## Epidemiology endpoints

We calculate the incidence rate ratio (IRR) and the incidence rate difference (IRD) per 1,000 person-months for various infection-related endpoints for each intervention scenario and compare them to the base case.
- **Endpoints**: Infections | Hospitalizations | ICU admissions | Deaths

Ensure that the file "```main_Epidem_Endpoints.R```" accesses the results of the simulation platform. In the example case, these are under the subfolder "```1_Simulation_Results```".
The outcome saves Excel files for the IRR and IRD for each intervention and endpoint.