# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 20:58:35 2022

@author: mejia
"""

import matplotlib.pyplot as plt
# import math  
# import time
import numpy as np
import pandas as pd
# import csv
# import statistics
# import scipy.stats
import seaborn as sns



Near_1 = pd.read_excel('data_arriv\TP_ED _Near.xlsx', 
                              index_col=0)

DF_near = pd.DataFrame(Near_1)

Tr_Pr = pd.read_excel (r'data_arriv\TP_ED _reduced.xlsx',
                       sheet_name = None)
DF_far = pd.DataFrame(Tr_Pr['5_Atte_NoN'])


DF_near.plot.line(figsize=(12,6))
plt.yscale('log')
plt.ylim([0.001, 100])
plt.rc('xtick', labelsize = 17) 
plt.rc('ytick', labelsize = 17) 
plt.legend(fontsize = 17)
plt.xlabel("Time (m)",fontsize = 17)
plt.title('Mean infection prob. (%) - Near-field', fontsize = 22)
# plt.savefig('figures/near_field_fin.svg', format='svg', dpi=1400)

ax1=plt.figure(2, figsize=(12,6), facecolor='w', edgecolor='k')
plt.semilogy(DF_far['m'], DF_far[1], '--', label='1 infected')
plt.semilogy(DF_far['m'], DF_far[3], '-.', label='3 infected')
plt.semilogy(DF_far['m'], DF_far[5], '-', label='5 infected')
plt.ylim([0.02, 40])
plt.xlim([0, 500])
plt.xlabel("Time (m)",fontsize = 17)
# plt.ylabel("B cells (counts)", fontsize=16)
plt.title('Far-field interactions', fontsize=22)
plt.rc('xtick', labelsize = 17) 
plt.rc('ytick', labelsize = 17) 
plt.legend(fontsize = 17)
# plt.legend(loc='upper left',fontsize=12)
# plt.savefig('figures/far_field_fin.svg', format='svg', dpi=1400)
plt.show()


