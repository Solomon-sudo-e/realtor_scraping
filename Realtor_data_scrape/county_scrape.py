import pandas as pd

data = pd.read_csv('uscounties.csv')

#print(data['county_full'])
#['state_name']['population']

new_data = pd.DataFrame({'county_full': data['county_full'], 'state_name': data['state_name'], 'population': data['population']})
print(new_data.info)
#print(new_data.dtypes)
for i in range(len(new_data)):
    if new_data.loc[i, 'population'] < 100000 or new_data.loc[i, 'population'] > 400000:
        new_data.drop([i], axis=0, inplace=True)
population_info_csv = new_data
#population_info_csv.to_csv('/Users/solomonhufford/Downloads')

from pathlib import Path  
filepath = Path('/Users/solomonhufford/csv_data')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
population_info_csv.to_csv(filepath)  
