import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
                sep = ',')

counties = ['Alameda', 'Contra Costa', 'Marin', 'Monterey', 'Napa', 'San Francisco',
           'San Joaquin', 'San Mateo', 'Santa Clara', 'Santa Cruz', 'Solano', 'Sonoma']

df = df[(np.isin(df['county'],counties)) & (df['state'] == 'California')]

df.sort_values(by = ['county', 'date'], inplace = True)

df.to_csv('bay_area_cases_deaths_clean.csv')
