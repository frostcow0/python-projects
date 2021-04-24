# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 21:43:50 2021

@author: gamet
"""
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error as mae
from sklearn.model_selection import train_test_split as tts
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

data=pd.read_csv(r'C:\Users\gamet\OneDrive\Documents\Data\owid-covid-data.csv')

test=trial_1=pd.read_pickle('covid_trial_1')
trial_2=pd.read_pickle('covid_trial_2')
test['Best MAEs 2']=trial_2['Best MAEs']
test['Difference']=test['Best MAEs']-test['Best MAEs 2']

# Works. Now, to do stuff >:)

"""
Data from the features needs cleaned. Yikes.
"""

#create initial DF
iso_codes=data.iso_code.unique()
iso_df=pd.DataFrame(iso_codes,columns=['ISO_Codes'])
#create labelencoder instance
labelencoder=LabelEncoder()
#assign numerical values and store in new column
iso_df['ISO_Codes_Cat']=labelencoder.fit_transform(iso_df['ISO_Codes'])

#This would hopefully finish the categorical->numerical change for iso codes
#data['iso_code']=iso_df['ISO_Codes_Cat']
data['iso_code_cat']=labelencoder.fit_transform(data['iso_code'])

data=data.fillna(0) # Trying to fill in the NAN spots with 0

# =============================================================================
# print('='*40)
# for k in data.columns:
#     print(k)
#     print('-'*40)
# =============================================================================
    
def model_creation(data,labels,features):
    logging.info('='*40)
    X=data[features]
    
    best_maes=[]
    
    for label in labels:
        logging.info('-'*40)
        y=data[label]
        logging.info('Beginning model testing for label {}.'.format(label))
        #best_model=None
        best_model_mae=999999999
        for i in range(7): # previously 15
            train_X,val_X,train_y,val_y=tts(X,y)
            
            model=RandomForestRegressor()
            
            model.fit(train_X,train_y)
            
            val_predictions=model.predict(val_X)
            val_mae=mae(val_predictions,val_y)
            
            if val_mae<best_model_mae:
                #best_model=model
                best_model_mae=val_mae
                logging.info('**New best model achieved below. Iteration #{}'.format(i))
                
            logging.info('Validation MAE: {:,.2f}'.format(val_mae))
        best_maes.append(best_model_mae)
    return best_maes

features=['iso_code_cat','extreme_poverty','gdp_per_capita','population',
          'aged_65_older','aged_70_older','cardiovasc_death_rate','diabetes_prevalence',
          'female_smokers','male_smokers']
info={
      'Labels':[]
      }

sus_labels=['new_deaths_per_million','new_deaths_smoothed_per_million',
            'reproduction_rate','weekly_icu_admissions','weekly_icu_admissions_per_million,',
            'positive_rate']



less_than_thou=['total_cases','new_cases']

less_than_hund=['']

less_than_ten=['']

less_than_one=['']

greater_than_thou=[label for label in info['Labels'] if label not in less_than_thou]

greater_than_thou2=list(filter(lambda x:x not in less_than_thou,info['Labels']))

accepted_datatypes=['float64','float32','int64','int32']
for category in data.columns:
    if data[category].dtype not in accepted_datatypes:
        logging.info('Category - {} - is the wrong dtype.'.format(category))
        continue
    if category not in features:
        info['Labels'].append(category)

# =============================================================================
# print('Labels being tested: ',info['Labels'])
# 
# info['Best MAEs']=model_creation(data,info['Labels'],features)
# 
# df=pd.DataFrame(info)
# 
# df.to_pickle('covid_trial_3')
# =============================================================================
