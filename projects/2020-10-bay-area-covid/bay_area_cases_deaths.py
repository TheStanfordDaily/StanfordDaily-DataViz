import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
                sep = ',')

counties = ['Alameda', 'Contra Costa', 'Marin', 'Monterey', 'Napa', 'San Francisco',
           'San Joaquin', 'San Mateo', 'Santa Clara', 'Santa Cruz', 'Solano', 'Sonoma']
populations = [1663000, 1147000, 260955, 437907, 140973, 884363, 745424, 
              770000, 1938000, 275897, 445458, 504217]

counties = pd.DataFrame({'county':counties, 'population':populations})

# filter the nyt dataset by the bay area counties
df = df[(np.isin(df['county'],counties)) & (df['state'] == 'California')]

df = pd.merge(df, counties, how = 'left', on = 'county')

df.sort_values(by = ['county', 'date'], inplace = True)

df[['cases_1000', 'deaths_1000']] = df[['cases', 'deaths']].div(df['population'].values, axis = 0)*1000

df[['new_cases', 'new_deaths']] = df.groupby(['county'])[['cases', 'deaths']].transform(lambda x: x.diff()) 
df[['roll_new_cases', 'roll_new_deaths']] = df.groupby('county')[['new_cases', 'new_deaths']].transform(lambda x: x.rolling(7, 1).mean())

df.to_csv('bay_area_cases_deaths_clean.csv')

#filter dataframe to Santa Clara only
scc = df[df['county'] == 'Santa Clara']

hosp  = pd.read_csv('https://data.sccgov.org/resource/5xkz-6esm.csv')

hosp = hosp[['date', 'icu_covid', 'covid_total_7davg', 'available_total', 'vents_pts', 'vents_available']]

hosp[['roll_icu_covid', 'roll_available_total']] = hosp[['icu_covid', 'available_total']].transform(lambda x: x.rolling(7, 1).mean())

hosp['date'] = pd.to_datetime(hosp.date)
scc['date'] = pd.to_datetime(scc.date)

scc = pd.merge(scc, hosp, on = 'date')

test = pd.read_csv('https://data.sccgov.org/resource/dvgc-tzgq.csv')

test.rename(columns = {'collection_date':'date'}, inplace = True)
test['date'] = pd.to_datetime(test.date)


test = test[['date', 'rate_pst_7d']]

scc = pd.merge(scc, test, on = 'date')

scc.to_csv('scc_cases_deaths_clean.csv')