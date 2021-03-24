# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 21:43:50 2021

@author: gamet
"""
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error as mae
from sklearn.model_selection import train_test_split as tts
import pandas as pd

data=pd.read_csv(r'C:\Users\gamet\OneDrive\Documents\Data\owid-covid-data.csv')

# Works. Now, to do stuff >:)

"""
Data from the features needs cleaned. Yikes.
"""


# =============================================================================
# print('='*40)
# for k in data.columns:
#     print(k)
#     print('-'*40)
# =============================================================================
    
features=['iso_code','location','total_cases','new_cases','icu_patients','new_tests','total_tests',
          'positive_rate']

y=data.extreme_poverty
X=data[features]

train_X,val_X,train_y,val_y=tts(X,y,random_state=23)

model=RandomForestRegressor(random_state=23)

model.fit(train_X,train_y)

val_predictions=model.predict(val_X)
val_mae=mean_absolute_error(val_predictions,val_y)

print('Validation MAE: {:,.2f}'.format(val_mae))