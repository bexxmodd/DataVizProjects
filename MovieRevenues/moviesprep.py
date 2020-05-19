import pandas as pd
import numpy as np

"""
link to the data I have obtained from IMDB webpage
is available in the .txt file located in this folder
"""
# import data
movies = pd.read_csv('tmdb_5000_movies.csv')
movies.head()

# let's start cleaning genres
movies['genres'].head()

# let's select only the columns I need
movies.columns
col = ['budget', 'genres', 'original_language', 'original_title', 'popularity',
       'production_countries', 'release_date', 'revenue', 'runtime', 'vote_average','vote_count']
movies = movies[col]

# First we should remove 'id' 'name' and 'number'
pattern = r'"id": [0-9]+, "name": '
movies['genres'] = movies['genres'].str.replace(pattern, '')

# I get rid of the brackets and the quotes
pattern1 = r'[\[{"+"}+\]]'
movies['genres'] = movies['genres'].str.replace(pattern1, '')
movies['genres'] = movies['genres'].str.replace(' ', '')

# Let's split the genre column for all the given genres
genres = movies['genres'].str.split(',', expand=True)

# I will only keep the first three genres for each movie, otherwise this thing can get overwhelming
genres = genres.iloc[:, :3]

# Replace column name for easier access
genres.replace({'ScienceFiction': 'Sci-Fi'}, inplace=True)

print(genres.describe())
print('number of rows in genres df: ', genres.shape[0])
print('number of rows in movies df: ',movies.shape[0])

# I combine our datasets into one df
movies_updated = pd.concat([movies, genres], axis=1)
movies = movies_updated.drop(['genres'], axis=1)
movies.rename(columns={0: 'main_genre',
                       1: 'secondary_genre',
                       2: 'tertiary_genre'},
              inplace=True)

# Clean the production countries and make it dataframe consistent
movies['production_countries'] = movies['production_countries'].str.extract(r'([A-Z]{2})')

# I will the information about the cast to the dataset from another csv file
cast = pd.read_csv('tmdb_5000_credits.csv')

# We want the information regarding the gender of the lead role
# for this I use regex method to extract needed data
cast_gender = cast['cast'].str.extract(r'(?<="gender":\s)([0-9])')
cast_gender.iloc[:, 0].value_counts(dropna=False)

# I'm replacing 0's with NaN values and males with 1
# this way we have binary variable with male=1 & female=0
cast_gender = cast_gender.replace('0', np.nan)
cast_gender = cast_gender.replace('2', '0')

cast_gender.iloc[:,0].value_counts(dropna=False)
cast_gender = cast_gender.astype(float, errors='ignore')

# I'm appending this column to our general dataset
movies_updated = pd.concat([movies, cast_gender], axis=1)
movies_updated.rename(columns={0: 'gender'}, inplace=True)
movies_updated.head()

# I will also scale the continiues budget and revenue variables
# This is more useful for  inferences as log'll be normally distributed
movies_updated['budget_log'] = np.log(movies_updated['budget'])
movies_updated['revenue_log'] = np.log(movies['revenue'])
movies_updated.info()


