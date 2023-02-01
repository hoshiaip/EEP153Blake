#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install plotly')
get_ipython().system('pip install wbdata')
get_ipython().system('pip install cufflinks')

import pandas
import wbdata
import plotly
import cufflinks 

from plotly.offline import init_notebook_mode, iplot

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# In[2]:


# population(year=2000,sex='Male',age_range=(0,100),place='WLD')
def population(year, sex, age_range, place):
    
    age_bins = [age_range[0], age_range[1]]
    
    # find the age ranges required
    age_ranges = []

    # Obtain lower end of lower age range
    if age_bins[0] % 5 != 0:
        age = 0
        while age_bins[0] - 5 > age:
            age = age + 5
        age_bins[0] = age
    
    # Ranges top out at 80, and go in five year increments
    for i in range(age_bins[0],age_bins[1],5):
        age_ranges.append(f"{i:02d}"+f"{i+4:02d}")

    if age_bins[1] >= 80:
        age_ranges.append("80UP")
    
    # determine indicators (age range + sex)
    variables = {}
    if sex=='Male':
        variables = {"SP.POP."+age_range+".MA":"Males "+age_range for age_range in age_ranges}
    elif sex=='Female':
        variables = {"SP.POP."+age_range+".FE":"Females "+age_range for age_range in age_ranges}
    else:
        variables = {"SP.POP."+age_range+".MA":"Males "+age_range for age_range in age_ranges}
        f_variables = {"SP.POP."+age_range+".FE":"Females "+age_range for age_range in age_ranges}
        variables.update(f_variables)
    
    # obtain relevant dataframe from wbdata
    df = wbdata.get_dataframe(variables, place)
    
    df = df.reset_index()
    df = df[df['date']==str(year)]
    
    #if age_range[0] > age_bins[0]:
    #    return (age_range[0] - age_bins[0]) / 5
    
    return df

population(year=2000, sex='Male', age_range=(67, 76), place='IND')


# In[3]:


vars = {"SE.PRM.ENRR.FE":"Female Primary School Enrollment"}


se = wbdata.get_dataframe(vars,country='IND')
se = se.reset_index()
se['date'] = se['date'].astype(int)
se = se.dropna()
print(se)

plt.plot('date', 'Female Primary School Enrollment', data=se, label='Primary Enrollment')
plt.xlabel('Date')
plt.ylabel('Enrollment (Base 2014-2016 = 100)')
plt.legend()
#plt.legend(['Female Primary School Enrollment'])


# In[4]:


#wbdata.get_indicator()
"""
Agriculture Production Indices:

AG.PRD.AGRI.XD                                     Agriculture production index (1999-2001 = 100)
AG.PRD.BLY.MT                                      Barley production (metric tons)
AG.PRD.CREL.MT                                     Cereal production (metric tons)
AG.PRD.CREL.XD                                     Cereal production index (1999-2001 = 100)
AG.PRD.CROP.XD                                     Crop production index (2014-2016 = 100)
AG.PRD.FNO.MT                                      Fonio production (metric tons)
AG.PRD.FOOD.XD                                     Food production index (2014-2016 = 100)
AG.PRD.GAGRI.XD                                    Agriculture production index (gross, 1999-2001 = 100)
AG.PRD.GCREL.XD                                    Cereal production index (gross, 1999-2001 = 100)
AG.PRD.GCROP.XD                                    Crop production index (gross, 1999-2001 = 100)
AG.PRD.GFOOD.XD                                    Food production index (gross, 1999-2001 = 100)
AG.PRD.GLVSK.XD                                    Livestock production index (gross, 1999-2001 = 100)
AG.PRD.GNFOOD.XD                                   Non-food production index (gross, 1999-2001 = 100)
AG.PRD.LVSK.XD                                     Livestock production index (2014-2016 = 100)
AG.PRD.MLT.MT                                      Millet production (metric tons)
AG.PRD.MZE.MT                                      Maize production (metric tons)
AG.PRD.NFOOD.XD                                    Gross non-food production index (1999-2001 = 100)
AG.PRD.RICE.MT                                     Rice production (metric tons)
AG.PRD.RTTB.MT                                     Roots and tubers production (metric tons)
AG.PRD.SGM.MT                                      Sorghum production (metric tons)
AG.PRD.WHT.MT                                      Wheat production (metric tons)
"""

vars = {"AG.PRD.LVSK.XD":"Livestock index",
        "AG.PRD.FOOD.XD":"Food index",
        "AG.PRD.CROP.XD":"Crop index",
        "SP.POP.TOTL":"Population"}


ag = wbdata.get_dataframe(vars,country='IND')
ag = ag.reset_index()
ag['date'] = ag['date'].astype(int)
print(ag)

lvsk = plt.plot('Population', 'Livestock index', data=ag, label='Livestock')
food = plt.plot('Population', 'Food index', data=ag, label='Food')
crop = plt.plot('Population', 'Crop index', data=ag, label='Crop')
plt.xlabel('Population')
plt.ylabel('Production (Base 2014-2016 = 100)')
plt.legend()
#plt.legend(['Livestock index', 'Food index', 'Crop index'])


# In[5]:


#plt.plot(ag['date'], np.log(ag['Population']))
#plt.plot(ag['date'], ag['Food index'])
ag_idx = ag.set_index(ag['date']).drop(columns=['date'])
ag_asc = ag_idx.sort_index()
ratesag = np.log(ag_asc).diff().dropna()
#ratesag
px.scatter(ratesag, x=ratesag.index, y=['Population', 'Food index'], trendline='ols')#, data=pop_growth_rate)
#px.scatter(ratesag, x=rates.index, y='Food index', trendline='ols')#, data=pop_growth_rate)


# In[6]:


ag_idx = ag.set_index(ag['date']).drop(columns=['date'])
ag_idx['Food index (log)'] = np.log(ag_idx['Food index'])
#ag_idx_log = np.log(ag_idx).dropna()
plt.scatter('Population', 'Food index (log)', data=ag_idx)
plt.xlabel('Population')
plt.ylabel('Food Production (log)')


# In[7]:


#plt.plot(se['date'], np.log(se['Female Primary School Enrollment']))
#plt.plot(se['date'], se['Food index'])
se_idx = se.set_index(se['date']).drop(columns=['date'])
se_asc = se_idx.sort_index()
ag_fdix = ag_idx
seag_merge = pandas.merge(ag_fdix, se_idx, on= "date")
#se_idx_log = np.log(se_idx).dropna()
plt.scatter('Female Primary School Enrollment', 'Food index (log)', data=seag_merge)
plt.xlabel('Female Primary School Enrollment')
plt.ylabel('Food Production (log)')

