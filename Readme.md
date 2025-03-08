# Loan Payment Prediction: End-to-End Machine Learning Project 🚀

This repository contains a comprehensive end-to-end machine learning pipeline for predicting loan payment outcomes. It covers the entire lifecycle of a data-driven project, from exploratory data analysis (EDA) and preprocessing to model development, deployment, and monitoring.

![seque (2)](https://github.com/user-attachments/assets/9ec830c6-adab-47fe-b510-9f4e2bc11999)


---

## Table of Contents
1. [Overview](#overview)  
2. [Project Workflow](#project-workflow)  
3. [Tech Stack](#tech-stack)  
4. [Detailed Steps](#detailed-steps)  
    - [1. Exploratory Data Analysis (EDA)](#1-exploratory-data-analysis-eda)  
    - [2. Data Preprocessing](#2-data-preprocessing)  
    - [3. Model Development](#3-model-development)  
    - [4. Experiment Tracking with MLflow](#4-experiment-tracking-with-mlflow)  
    - [5. API Deployment with FastAPI](#5-api-deployment-with-fastapi)  
    - [6. Frontend Visualization with Streamlit](#6-frontend-visualization-with-streamlit)  
    - [7. Monitoring with Arize AI](#7-monitoring-with-arize-ai)  
5. [How to Run the Project](#how-to-run-the-project)  
6. [Future Enhancements](#future-enhancements)

---

## Overview
This project focuses on building a predictive system for determining loan payment outcomes. The pipeline is designed to handle real-world complexities like missing data, imbalanced classes, and scalable deployment. 

### Key Objectives:
- Build a robust machine learning model for loan payment prediction.
- Deploy the model using FastAPI for integration with external systems.
- Provide an interactive Streamlit dashboard for users to visualize predictions and explore insights.
- Implement model monitoring with Arize AI to ensure consistent performance post-deployment.

---

## Project Workflow
1. Data Analysis and Preprocessing.
2. Model Development and Evaluation.
3. Experiment Tracking with MLflow.
4. API Deployment for Predictions.
5. Interactive Dashboard for End Users.
6. Continuous Monitoring and Feedback Loop.

---

## Tech Stack
- **Programming Language:** Python  
- **Libraries:** Pandas, NumPy, Scikit-learn, XGBoost, FastAPI, Streamlit  
- **Model Tracking:** MLflow  
- **Deployment Tools:** Streamlit 
- **Monitoring:** Arize AI  

---

## Detailed Steps

### 1. Exploratory Data Analysis (EDA)
The EDA phase involves understanding the dataset and identifying patterns, trends, and outliers. Key steps include:
- **Descriptive Statistics:** Examining distributions, correlations, and feature relationships.
- **Visualizations:** Creating histograms, scatter plots, and heatmaps for insights.
- **Class Imbalance Analysis:** Understanding the distribution of payment outcomes.

  NB.: You can find the dataset in this link: https://www.kaggle.com/datasets/mirbektoktogaraev/should-this-loan-be-approved-or-denied

**Tools Used:** Matplotlib, Seaborn, Pandas Profiling.

---

### 2. Data Preprocessing
To prepare the data for model training:
- **Handling Missing Values:** Using imputation techniques.
- **Feature Engineering:** Creating new features like loan-to-income ratio.
- **Scaling and Encoding:** Normalizing numeric data and encoding categorical variables.
- **Train-Test Split:** Dividing the dataset into training and testing sets.
- **Oversampling:** Addressing class imbalance using SMOTE.

**Tools Used:** Scikit-learn, Imbalanced-learn.

---

### 3. Model Development
A range of models was developed and evaluated to identify the best-performing algorithm:
- **Algorithms Tested:** Logistic Regression, Random Forest, XGBoost.
- **Evaluation Metrics:** Accuracy, Precision, Recall, F1 Score, ROC-AUC.

**Final Model:** XGBoost was selected for its superior performance and interpretability.

**Tools Used:** Scikit-learn, XGBoost.

---

### 4. Experiment Tracking with MLflow
To ensure reproducibility and effective experiment tracking:
- **Tracking Metrics:** Capturing key metrics like accuracy, precision, and recall.
- **Logging Parameters:** Storing hyperparameters for each run.
- **Model Registry:** Saving the best-performing model for deployment.

**Tools Used:** MLflow, SQLite (for backend storage).

---

### 5. API Deployment with FastAPI
A FastAPI-based RESTful API was developed for seamless model integration:
- **Endpoints:**  
  - `/predict`: Accepts JSON payloads and returns loan payment predictions.  
  - `/health`: Monitors API health.  
- **Dockerized Deployment:** Ensures portability across environments.

**Tools Used:** FastAPI, Uvicorn.

---

### 6. Frontend Visualization with Streamlit
An interactive dashboard allows users to explore model predictions and dataset insights:
- **Features:**
  - Upload new datasets and receive predictions.
  - Visualize feature importance and model metrics.
  - Analyze dataset trends and distributions.

**Tools Used:** Streamlit.

---

### 7. Monitoring with Arize AI
Post-deployment monitoring ensures the model continues to perform well in production:
- **Logged Data:** Training and inference datasets with features, predictions, and actual outcomes.
- **Key Metrics Tracked:** Accuracy drift, data drift, feature importance changes.
- **Integration:** Arize AI was used for setting up model monitoring and alerting systems.

**Tools Used:** Arize AI SDK.

---

## How to Run the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/missaouimedamine/Mlops.git
   cd Mlops
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MLflow Tracking Server**:
   ```bash
   mlflow ui
   ```

4. **Run FastAPI Server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Launch Streamlit Dashboard**:
   ```bash
   streamlit run main.py
   ```

6. **Monitor with Arize AI**:
   - Ensure Arize keys are set up in your environment variables.
   - View logged data on the [Arize Dashboard](https://app.arize.com/).

---

## Future Enhancements
- **Advanced Hyperparameter Tuning:** Use Bayesian Optimization or Hyperopt.
- **Real-Time Predictions:** Integrate Kafka or RabbitMQ for streaming data.
- **Enhanced Monitoring:** Incorporate advanced drift detection techniques.
- **Support for Multiple Models:** Extend the pipeline for handling multiple model versions.

---

Feel free to contribute to this project by submitting pull requests or raising issues. 😊
