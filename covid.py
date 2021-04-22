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

data=pd.read_csv(r'C:\Users\gamet\OneDrive\Documents\Data\owid-covid-data.csv')

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
    
features=['iso_code_cat','total_cases_per_million','icu_patients','total_tests_per_thousand',
          'positive_rate','total_deaths_per_million','tests_per_case']

y=data.extreme_poverty
X=data[features]

best_model=None
best_model_mae=1

for i in range(10):
    train_X,val_X,train_y,val_y=tts(X,y) # random_state=23 gets 0.33
    
    model=RandomForestRegressor() # random_state=23 gets 0.33
    
    model.fit(train_X,train_y)
    
    val_predictions=model.predict(val_X)
    val_mae=mae(val_predictions,val_y)
    
    if val_mae<best_model_mae:
        best_model=model
        best_model_mae=val_mae
        print("-"*10,"New best model achieved below. Iteration #{}".format(i))
        
    print('Validation MAE: {:,.2f}'.format(val_mae))

    
