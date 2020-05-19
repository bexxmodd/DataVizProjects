# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:40:21 2020

@author: Hellrox
"""

import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

auth = {'9DD13B127BA34FF4C72C398E136997F2'}
headers={'Content-Type':'application/json'}
bcs_url = 'https://www.breakingbadapi.com/api/characters?category=Better+Call+Saul'
resp = requests.get(bcs_url, headers=headers)
print(resp.status_code)


# breaking bad characters
bb_url = 'https://www.breakingbadapi.com/api/characters?category=Breaking+Bad'
resp1 = requests.get(bb_url, headers=headers).json()

# Death Count  
death_url = 'https://www.breakingbadapi.com/api/deaths/'
resp = requests.get(death_url, headers=headers).json()
resp[:10]

death_df = pd.DataFrame(json_normalize(resp))
death_df.head(10)

death_df.shape

pivot = pd.pivot_table(death_df, values='number_of_deaths',
            index=['season', 'episode'], aggfunc=np.sum)
print(pivot)

# lets plot death numbers
def to_episode(col):
    episodes = ['E0' + str(c) if c < 10 else 'E' + str(c) for c in col]
    return episodes

def season_episode(col1, col2):
    season_episode = []
    col01 = ['S'+ str(s) for s in col1]
    col02 = to_episode(col2)
    for s, e in zip(col01, col02):
        season_episode.append(s + e)
    return season_episode

season_episode(death_df['season'].values, death_df['episode'].values)

death_df['season_episode'] = season_episode(death_df['season'].values, death_df['episode'].values)

ddf = death_df[death_df.columns[-2:]]
ddf = ddf.groupby('season_episode').sum()
ddf.reset_index(inplace=True)

# plotting the bar chart for the death per episode
clrs = ['red' if x >= 10 else 'grey' for x in ddf['number_of_deaths']]

fig, ax = plt.subplots(figsize=(10,6))
ax.bar(ddf['season_episode'], ddf['number_of_deaths'], color=clrs)
ax.set_ylim(0, 20)
plt.xticks(rotation=45)
ax.set_xlabel('Season-Episode')
ax.set_ylabel('Number of Deaths')
ax.set_title('Deaths in Breaking Bad', fontsize = 16)
plt.yticks(range(0, 21, 2))


"""
Now lets look at the Death Count by individual

"""
url = 'https://www.breakingbadapi.com/api/characters?category=Breaking+Bad'
resp = requests.get(url, headers=headers).json()

df = json_normalize(resp)
df = pd.DataFrame(df)
df.head()

# I will extract character names
def name_extractor(df):
    """
    adding '+' in beetween to adhere to the API endpoint standard
    
    """
    chars = df.str.replace(' ', '+')
    return chars

# using 'name_extractor()' I exctract values from the API
# and aggregate them in a new dictionary
def get_death_count():
    names = name_extractor(df['name']) # Executing 'name_extractor()' function
    death_count = {}
    url = 'https://www.breakingbadapi.com/api/death-count?name='
    for n in names:
        url_new = url + n
        resp = requests.get(url_new).json()
        death_count[n] = resp
    return death_count


def counter():
    """
    I extract the dictionary which is nested inside the list
    move it to the new dict which has two keys
    name and death count
    
    """
    chars = get_death_count()
    counted = {}
    for name in chars:
        number = chars[name][0]['deathCount']
        counted[name] = number
    return counted

data = counter()

# convert data into dataframe and prepare for plotting
df1 = pd.DataFrame.from_dict(data, orient='index')
df_bb = df1[df1[0] != 0]
df_bb.reset_index(inplace=True)
df_bb.rename(columns={'index': 'name', 0: 'number_of_deaths'}, inplace=True)
df_bb['name'] = df_bb['name'].str.replace('+', ' ')
df_bb = df_bb.sort_values(by='number_of_deaths', ascending=True)


# finally plot the graph
clrs = ['red' if x >= 30 else 'grey' for x in df_bb['number_of_deaths']]
plt.barh(df_bb['name'], df_bb['number_of_deaths'], color=clrs)
plt.xlabel('Number of Deaths')
plt.title('Breaking Bad Characters and Deaths Count')
plt.show()













