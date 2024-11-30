from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sklearn
from fastapi import FastAPI, File, UploadFile
import uvicorn
import sys  
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mlflow
from src.clean_data_json import scaling,clean_data
#from src.clean_data_json import clean_data_json
from example_json.transaction_info import TransactionModel
import mlflow.pyfunc






"""
from dotenv import load_dotenv
import os
load_dotenv("../backend/src/.env")

DagsHub_username = os.getenv("DagsHub_username")
DagsHub_token=os.getenv("DagsHub_token")
os.environ['MLFLOW_TRACKING_USERNAME']= DagsHub_username
os.environ["MLFLOW_TRACKING_PASSWORD"] = DagsHub_token
"""

#setup mlflow
mlflow.set_tracking_uri("file:///C:/Users/msi/Desktop/mlops/mlruns")
mlflow.set_experiment("loan_approval_prediction")
mlflow.sklearn.autolog(disable=True)

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#let's call the model from the model registry ( in production stage)

df_mlflow=mlflow.search_runs(filter_string="metrics.F1_score_test < 1")
run_id = '508f98877c244ee58b2ee59373384b32'



logged_model = f'runs:/{run_id}/ML_models'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

@app.get("/")
def read_root():
    return {"Hello": "to fraud detector app version 2"}

# this endpoint receives data in the form of csv file (histotical transactions data)
@app.post("/predict/csv")
def return_predictions(file: UploadFile = File(...)):
    data = pd.read_csv(file.file)
    data=data.drop(columns=['Unnamed: 0','Default'])
    preprocessed_data = clean_data(data)
    scaled=scaling(preprocessed_data)
    predictions = model.predict(scaled)
    return {"predictions": predictions.tolist()}


# this endpoint receives data in the form of json (informations about one transaction)
@app.post("/predict")
def predict(data : TransactionModel):
    received = data.dict()
    df =  pd.DataFrame(received,index=[0])
    scl=clean_data(df)
    preprocessed_data = scaling(scl)
    print(preprocessed_data)
    predictions = model.predict(preprocessed_data)
    return {"predictions": predictions.tolist()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)


