import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#from sklearn.preprocessing import TargetEncoder
#import category_encoders as ce
#import streamlit as sk

# import data
df =  pd.read_csv('cars24-car-price.csv')
print(df.head())

# create encoding for categorical data 
# target encoding
#target_encode = ce.TargetEncoder()
encode_dict={
    "fuel_type": {"Diesel": 1, "Petrol": 2, "CNG": 3, "LPG": 4, "Electric": 5},
     "transmission_type": {"Manual": 1, "Automatic": 2},
	 "seller_type": {"Dealer": 1, "Individual": 2, "Trustmark Dealer": 3}

     }

df.replace(encode_dict, inplace=True)
df.head()
features = ['year', 'seller_type', 'km_driven', 'fuel_type', 'transmission_type', 'mileage', 'engine', 'max_power', 'seats']
target = ['selling_price']

X = df[features]
y = df[target]

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)

# dump scaler object using joblib
import joblib
joblib.dump(scaler, 'scaler.pkl')

# train decision tree model
from sklearn.tree import DecisionTreeRegressor
# don't bother with train-test

model = DecisionTreeRegressor()
model.fit(X, y)

# dump model using joblib

import joblib
joblib.dump(model, 'cars24-car-price-model.joblib')

import pickle
pickle.dump(model, open('cars24-car-price-model.pkl', 'wb'))

