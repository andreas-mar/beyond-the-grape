#Wines
import json
import os
import pandas as pd
import numpy as np

def vivino_json_to_df(file):
    with open(file) as f:
        data = json.load(f)
        taste_structures = dict()
        flavors = dict()
        rank1 = []
        rank2 = []
        foods = []
        food_options = []
        for item in data:
            try:
                rank1.append(data[item]['rank'][0])
            except:
                rank1.append(np.nan)

            try:
                rank2.append(data[item]['rank'][1])
            except:
                rank2.append(np.nan)

            separator = ', '
            foods.append(separator.join(data[item]['foods']))
            
            flavors[item] = data[item]['flavor']
            taste_structures[item] = data[item]['taste_structure']
            
            for item in data[item]['foods']:
                if not item in food_options: 
                    food_options.append(item)  
                
        df = pd.DataFrame.from_dict(data).T
        df['foods'] = foods
        
        df['top_world_pct'] = rank1
        df['top_world_pct'] = df['top_world_pct'].str.extract('(\d+)')
        df['top_region_pct'] = rank2
        df['top_region_pct'] = df['top_region_pct'].str.extract('(\d+)')
        
        df['price'] = df['price'].str.replace(' kr.', '')
        df['price'] = df['price'].astype(float)
        
        taste_structures_df = pd.DataFrame.from_dict(taste_structures).T
        taste_structures_df.reset_index(inplace=True)
        taste_structures_df.rename(columns={'index': 'wine_id'}, inplace=True)
        
        flavors_df = pd.DataFrame.from_dict(flavors).T
        flavor_options = flavors_df.columns 
        flavors_df.reset_index(inplace=True)
        flavors_df.rename(columns={'index': 'wine_id'}, inplace=True)
        
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'wine_id'}, inplace=True)
        
        df = pd.merge(df, taste_structures_df, on='wine_id', how='outer')
        df = pd.merge(df, flavors_df, on='wine_id', how='outer')
        
        #Creating dummy columns
        for i in food_options:
            df[i] = df['foods'].str.contains(pat = i)
            df[i] = df[i].astype(int)
        
        df['total_flavors'] = 0
        #Averaing flavors
        #print(flavor_options)
        
        #Need error handling here.
        #for col in flavor_options:
        #    df['total_flavors'] = df['total_flavors'] + df[col]
        
        del df['taste_structure']
        del df['flavor']
        del df['rank']
        del df['iterations']
        return df

os.chdir('./Selenium_data')

df = pd.DataFrame()
for file in os.listdir():
    if file.endswith('.json'):
        df = df.append(vivino_json_to_df(file))

df = df.drop_duplicates(subset='wine_id', keep='first')
df.to_csv('Combined_selenium.csv')

print(df.shape)



