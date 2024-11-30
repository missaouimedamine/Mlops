import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
scale = StandardScaler()
def convert_money(x):
    if isinstance(x, str):  # Check if x is a string
        x = x[1:].replace(',', '')  # Remove the dollar sign and commas
        return float(x)
    elif isinstance(x, (int, float)):  # If already numeric, return as is
        return float(x)
    else:
        return None  # Handle unexpected types gracefully

def clean_year(x):
    if isinstance(x, str):
        return x.replace('A', '')
    return x

with open("../backend/src/store.json", "r") as file:
    x = json.load(file)

def transform_data(df):
    df[['DisbursementGross', 'BalanceGross', 'ChgOffPrinGr', 'GrAppv', 'SBA_Appv']] = df[['DisbursementGross', 'BalanceGross', 'ChgOffPrinGr', 'GrAppv', 'SBA_Appv']].applymap(convert_money)
    df['State'] = df['State'].map(x['State'])
    df['BankState'] = df['BankState'].map(x['BankState'])
    df['Industry'] = df['Industry'].map(x['Industry'])
    df['ApprovalFY'] = df['ApprovalFY'].apply(clean_year).astype('int64')
    df.dropna(subset=['Name', 'City', 'State', 'BankState', 'NewExist','RevLineCr', 'LowDoc', 'DisbursementDate', 'MIS_Status'], inplace=True)
    df = df.astype({'Zip': 'str', 'NewExist': 'int64', 'UrbanRural': 'str', 'DisbursementGross': 'float', 'BalanceGross': 'float',
                          'ChgOffPrinGr': 'float', 'GrAppv': 'float', 'SBA_Appv': 'float'})
    df['Industry'] = df['NAICS'].astype('str').apply(lambda x: x[:2])
    df['Industry'] = df['Industry'].map({
    '0':'Unknown',
    '11': 'Ag/For/Fish/Hunt',
    '21': 'Min/Quar/Oil_Gas_ext',
    '22': 'Utilities',
    '23': 'Construction',
    '31': 'Manufacturing',
    '32': 'Manufacturing',
    '33': 'Manufacturing',
    '42': 'Wholesale_trade',
    '44': 'Retail_trade',
    '45': 'Retail_trade',
    '48': 'Trans/Ware',
    '49': 'Trans/Ware',
    '51': 'Information',
    '52': 'Finance/Insurance',
    '53': 'RE/Rental/Lease',
    '54': 'Prof/Science/Tech',
    '55': 'Mgmt_comp',
    '56': 'Admin_sup/Waste_Mgmt_Rem',
    '61': 'Educational',
    '62': 'Healthcare/Social_assist',
    '71': 'Arts/Entertain/Rec',
    '72': 'Accom/Food_serv',
    '81': 'Other_no_pub',
    '92': 'Public_Admin'
})
    df.dropna(subset=['Industry'], inplace=True)
    df.loc[(df['FranchiseCode'] <= 1), 'IsFranchise'] = 0
    df.loc[(df['FranchiseCode'] > 1), 'IsFranchise'] = 1
    df = df.astype({'IsFranchise': 'int64'})
    df = df[(df['NewExist'] == 1) | (df['NewExist'] == 2)]

# Create NewBusiness field where 0 = Existing business and 1 = New business; based on NewExist field
    df.loc[(df['NewExist'] == 1), 'NewBusiness'] = 0
    df.loc[(df['NewExist'] == 2), 'NewBusiness'] = 1
    df = df[(df['RevLineCr'] == 'Y') | (df['RevLineCr'] == 'N')]
    df = df[(df['LowDoc'] == 'Y') | (df['LowDoc'] == 'N')]

# RevLineCr and LowDoc: 0 = No, 1 = Yes
    df['RevLineCr'] = np.where(df['RevLineCr'] == 'N', 0, 1)
    df['LowDoc'] = np.where(df['LowDoc'] == 'N', 0, 1)
    df['Default'] = np.where(df['MIS_Status'] == 'P I F', 0, 1)
    df[['ApprovalDate', 'DisbursementDate']] = df[['ApprovalDate', 'DisbursementDate']].apply(pd.to_datetime)
    df['DisbursementFY'] = df['DisbursementDate'].map(lambda x: x.year)
    df['DaysToDisbursement'] = df['DisbursementDate'] - df['ApprovalDate']
    df['DaysToDisbursement'] = df['DaysToDisbursement'].astype('str').apply(lambda x: x[:x.index('d') - 1]).astype('int64')
    df['SBA_AppvPct'] = df['SBA_Appv'] / df['GrAppv']
    df['AppvDisbursed'] = np.where(df['DisbursementGross'] == df['GrAppv'], 1, 0)
    df = df.astype({'IsFranchise': 'int64', 'NewBusiness': 'int64'})
    df.drop(columns=['LoanNr_ChkDgt', 'Name', 'City', 'Zip', 'Bank', 'NAICS', 'ApprovalDate', 'NewExist', 'FranchiseCode',
                      'ChgOffDate', 'DisbursementDate', 'BalanceGross', 'ChgOffPrinGr', 'SBA_Appv', 'MIS_Status','CreateJob','RetainedJob'], inplace=True)
    # Field for loans backed by Real Estate (loans with a term of at least 20 years)
    df['RealEstate'] = np.where(df['Term'] >= 240, 1, 0)

# Field for loans active during the Great Recession (2007-2009)
    df['GreatRecession'] = np.where(((2007 <= df['DisbursementFY']) & (df['DisbursementFY'] <= 2009)) | 
                                     ((df['DisbursementFY'] < 2007) & (df['DisbursementFY'] + (df['Term']/12) >= 2007)), 1, 0)
    df['DisbursedGreaterAppv'] = np.where(df['DisbursementGross'] > df['GrAppv'], 1, 0)
    for column in df.select_dtypes(include='object').columns:
    # Encode the column
        df[column] = encoder.fit_transform(df[column])
    y = df['Default']
    X = df.drop('Default', axis=1)
    return X,y


