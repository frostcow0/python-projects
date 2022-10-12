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

trial_1=pd.read_pickle('covid_trial_1')
trial_2=pd.read_pickle('covid_trial_2')
latest_trial=trial_3=pd.read_pickle('covid_trial_3')

# Works. Now, to do stuff >:)

"""
Data from the features needs cleaned. Yikes.
"""
features=['iso_code_cat','extreme_poverty','gdp_per_capita','population',
          'aged_65_older','aged_70_older','cardiovasc_death_rate','diabetes_prevalence',
          'female_smokers','male_smokers']

def iso_code_conversion():
    global data
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
        logging.info('Beginning model testing for label {0}. {1}% Complete.'.format(label))
        #best_model=None
        best_model_mae=999999999
        for i in range(25): # previously 15
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

def label_setup():

    labels={
          'usable':[],
          'new_test_labels':[]
          }
    
    filter1=latest_trial['Best MAEs']<=1000
    filter2=latest_trial['Best MAEs']>=0.5
    latest_trial.where(filter1&filter2,inplace=True)
    
    accepted_datatypes=['float64','float32','int64','int32']
    for category in data.columns:
        if data[category].dtype not in accepted_datatypes:
            logging.info('Category - {} - is the wrong dtype.'.format(category))
            continue
        if category not in features:
            labels['usable'].append(category)
            if len(latest_trial[latest_trial['new_test_labels']==category]):
                labels['new_test_labels'].append(category)
            
    return labels

iso_code_conversion()
labels=label_setup()

labels['Best MAEs']=model_creation(data,labels['new_test_labels'],features)

df=pd.DataFrame(labels)

df.to_pickle('covid_trial_3')
