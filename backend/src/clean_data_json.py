import json
import pandas as pd
from sklearn.preprocessing import StandardScaler

scale = StandardScaler()


with open("../backend/src/store.json", "r") as file:
    x = json.load(file)
def clean_data(df):
    df['State'] = df['State'].map(x['State'])
    df['BankState'] = df['BankState'].map(x['BankState'])
    df['Industry'] = df['Industry'].map(x['Industry'])
    return df

# Function to scale data
def scaling(df):
    # Only scale numerical columns
    num_cols = df.select_dtypes(include=['number']).columns
    df[num_cols] = scale.fit_transform(df[num_cols])
    return df
