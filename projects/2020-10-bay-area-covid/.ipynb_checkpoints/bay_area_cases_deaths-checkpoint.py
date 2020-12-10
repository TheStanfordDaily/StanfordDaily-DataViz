import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
                sep = ',')

counties = ['Alameda', 'Contra Costa', 'Marin', 'Monterey', 'Napa', 'San Francisco',
           'San Joaquin', 'San Mateo', 'Santa Clara', 'Santa Cruz', 'Solano', 'Sonoma']

df = df[(np.isin(df['county'],counties)) & (df['state'] == 'California')]

df.sort_values(by = ['county', 'date'], inplace = True)

df['new_cases'] = df.groupby(['county'])['cases'].transform(lambda x: x.diff()) 
df['new_deaths'] = df.groupby(['county'])['deaths'].transform(lambda x: x.diff()) 

#get moving averages of cases, deaths, new_cases, new_deaths
df['roll_new_cases'] = df.groupby('county')['new_cases'].transform(lambda x: x.rolling(7, 1).mean())
df['roll_new_deaths'] = df.groupby('county')['new_deaths'].transform(lambda x: x.rolling(7, 1).mean())

df.to_csv('bay_area_cases_deaths_clean.csv')

scc = df[df['county'] == 'Santa Clara']
scc.to_csv('scc_cases_deaths_clean.csv')
