# -*- coding: utf-8 -*-
"""
Created on Sat May  2 09:47:12 2020

@author: Hellrox
"""

import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt

# open csv file
df = pd.read_csv('Electricity_Maryland.csv')

def split_columns(df):
    
    percent = [df.columns[0]]
    amount = []
    
    for col in df.columns:
        if re.search(r'%', col):
            percent.append(col)
        else:
            amount.append(col)
    return percent, amount
        

def split_df(df):
    percents, amounts = split_columns(df)
    df_perc = df[percents]
    df_mwh = df[amounts]
    return df_perc, df_mwh

df_perc, df_mwh = split_df(df)

df_perc.set_index('Energy Source', inplace=True)
df_perc = df_perc.T
df_perc = df_perc.add_suffix(' (%)')
df_perc['Biomass (%)'] = df_perc['Other Biomass (%)'] + df_perc['Wood (%)']

df_mwh.set_index('Energy Source', inplace=True)
df_mwh = df_mwh.T
df_mwh = df_mwh.add_suffix(' (MWh)')
df_mwh['Biomass (MWh)'] = df_mwh['Other Biomass (MWh)'] + df_mwh['Wood (MWh)']

df_perc.reset_index(inplace=True)
df_perc['index'] = df_perc['index'].str.split(' ').str[0]

df_mwh.reset_index(inplace=True)
df_mwh['index'] = df_mwh['index'].str.split(' ').str[0]

merged = pd.merge(df_mwh, df_perc, on=['index'])

merged = merged.drop(['Other Biomass (MWh)', 'Wood (MWh)',
                       'Other Biomass (%)', 'Wood (%)'],
                     axis=1)

merged.rename(columns={'index': 'Year'}, inplace=True)
merged['Year'] = merged['Year'].astype(int)



# assigning emissions

merged['Coal_CO2_kg'] = merged['Coal (MWh)'] * 109
merged['Hydroelectric_CO2_kg'] = merged['Hydroelectric (MWh)'] * 97
merged['Natural_Gas_CO2_kg'] = merged['Natural Gas (MWh)'] * 79
merged['Biomass_CO2_kg'] = merged['Biomass (MWh)'] * 98
merged['Petroleum_CO2_kg'] = merged['Petroleum (MWh)'] * 184
merged['Solar_CO2_kg'] = merged['Solar (Utility scale only) (MWh)'] * 6
merged['Wind_CO2_kg'] = merged['Wind (MWh)'] * 4
merged['Nuclear_CO2_kg'] = merged['Nuclear (MWh)'] * 2


# creating per capita income
income_data = {'Year': [i for i in range(1990, 2018)],
               'per_capita': [23104, 23605, 24503, 25239, 26161, 27070, 28119, 29432,
                              31486, 33124, 35681, 37157, 38170, 39524, 41862, 43481,
                              45932, 47586, 49428, 48755, 50007, 52433, 53547, 53057,
                              54695, 57150, 59042, 60522]}
income = pd.DataFrame(income_data)

complete = pd.merge(merged, income, on=['Year'])

complete.to_excel('energy_complete.xlsx')

co2_gram = {'Coal': 109, 'Hydroelectric': 97, 'Natural Gas': 79,
            'Biomass': 98, 'Petroleum': 184, 'Solar': 6,
            'Wind': 4, 'Nuclear': 2}

co2_scale = pd.DataFrame.from_dict(co2_gram, orient='index')
co2_scale.reset_index(inplace=True)
co2_scale = co2_scale.rename(columns={'index': 'Energy Source', 0: 'CO2e/kWh'})


# plot bar chart
co2_scale.sort_values('CO2e/kWh', inplace=True)

fig, ax = plt.subplots(figsize=(9, 5))

# clrs = ['red' if x >= 30 else 'grey' for x in df_bb['number_of_deaths']]
clrs = ['red' if x > 100 else 'grey' for x in co2_scale['CO2e/kWh']]
ax.barh(co2_scale['Energy Source'], co2_scale['CO2e/kWh'], color=clrs)
ax.set_title('Emissions Footprint Per Energy Source', size=16)
ax.set_xlabel('gCO2e/kWh')

fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.plot(complete['Year'], complete['per_capita'], '-o', color='red')
ax1.set_title('Per Capita Income - Nominal Dollars')
ax1.set_ylabel('$US')


# total emissions

sum_co2 = complete.iloc[:, -9:-1].sum(axis=1)
co2_change = sum_co2.pct_change()*100


fig, axz = plt.subplots(1,2, figsize=(16, 6))
fig.suptitle('The State of Maryland', fontsize=20)

axz[0].plot(complete['Year'], sum_co2, color='orange', linewidth=3)
axz[0].set_title('Total CO2e Emission', size=14)
axz[0].set_ylabel('Metric Tons of CO2')
axz[0].set_xlim(1990, 2018)

clrs2 = ['red' if x > 0 else 'green' for x in co2_change]
axz[1].bar(complete['Year'], co2_change, color=clrs2)
axz[1].set_title('CO2e Emission % Change', size=14)
axz[1].set_xlim(1990, 2018)
axz[1].set_ylabel('Percentage Change')
# plt.tight_layout()

# Perform ARIMA.
from statsmodels.tsa.arima_model import ARIMA

non_renew = complete.loc[:, ['Coal_CO2_kg', 'Hydroelectric_CO2_kg',
                       'Natural_Gas_CO2_kg', 'Petroleum_CO2_kg']].sum(axis=1)
non_renew = non_renew.to_frame()

non_renew['Year'] = [i for i in range(1990, 2018)]
non_renew = non_renew[['Year', 0]]

model = ARIMA(non_renew[0], order=(5, 1, 0))
model_fit = model.fit(disp=0)
print(model_fit.summary())

residuals = pd.DataFrame(model_fit.resid)
residuals.plot(color='r')
plt.show()
residuals.plot(kind='kde', color='r')
plt.show()
print(residuals.describe())



# Pie chart
labels = 'Solar', 'Coal', 'Nuclear', 'Other Non-Renewables', 'Renewables'
size1 = [0.1, 54.3, 32.1, 8.4, 5.1]
colors= ['red', 'grey', 'dimgrey', 'lightgrey', 'darkgrey']
explode = (0.1, 0, 0, 0, 0)

fig, axx = plt.subplots(1,2, figsize=(12,6))
axx[0].pie(size1, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=145)
axx[0].set_title('2010', fontsize=18)

size = [7.8, 24.4, 43.4, 20.5, 3.9]
axx[1].pie(size, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=140)
axx[1].set_title('2017', fontsize=18)
plt.show()




