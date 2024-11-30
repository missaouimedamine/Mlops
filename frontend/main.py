import requests
import streamlit as st
import json
import pandas as pd

# Load configuration data from JSON
with open("backend/src/store.json", "r") as file:
    x = json.load(file)

# Page Title
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

# Helper function to map Yes/No to 1/0
def gett(choice):
    return 1 if choice == "Yes" else 0

# Load configuration data from JSON
with open("backend/src/store.json", "r") as file:
    x = json.load(file)

# Load the data
@st.cache_data
def load_data():
    file_path = "data/loan_data.csv"  # Update this with your file path
    return pd.read_csv(file_path)

df = load_data()

# Sidebar with radio buttons for navigation
sidebar_option = st.sidebar.radio("Select Page", ["Dashboard", "Prediction"])

if sidebar_option == "Dashboard":
    # Dashboard Page
    st.title("SBA Loans Dashboard")
    st.markdown("Explore loan trends, analyze defaults, and gain insights into SBA loan data.")
    
    # Sidebar Filters for Dashboard
    st.sidebar.header("Filters")
    states = st.sidebar.multiselect("Select State(s):", df["State"].unique(), default=df["State"].unique())
    industries = st.sidebar.multiselect("Select Industry(s):", df["Industry"].unique(), default=df["Industry"].unique())
    approval_year = st.sidebar.slider("Approval Fiscal Year Range:", 
                                       int(df["ApprovalFY"].min()), 
                                       int(df["ApprovalFY"].max()), 
                                       (int(df["ApprovalFY"].min()), int(df["ApprovalFY"].max())))
    
    # Filter Data
    filtered_data = df[(df["State"].isin(states)) & 
                       (df["Industry"].isin(industries)) & 
                       (df["ApprovalFY"] >= approval_year[0]) & 
                       (df["ApprovalFY"] <= approval_year[1])]
    
    # Overview Metrics
    st.header("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Loans", len(filtered_data))
    col2.metric("Default Rate", f"{(filtered_data['Default'].mean() * 100):.2f}%")
    col3.metric("Avg Loan Amount", f"${filtered_data['DisbursementGross'].mean():,.2f}")
    col4.metric("Franchise Loans", f"{filtered_data['IsFranchise'].sum()}")
    
    # Visualizations
    st.header("Visualizations")

    # Loan Distribution by State
    fig_state = px.bar(filtered_data.groupby("State").size().reset_index(name="Loans"), 
                       x="State", y="Loans", title="Loan Distribution by State")
    st.plotly_chart(fig_state)

    # Loan Amount vs Default Rate
    fig_default = px.scatter(filtered_data, 
                             x="DisbursementGross", y="Default", 
                             color="Industry", 
                             title="Loan Amount vs Default Rate", 
                             size="GrAppv", hover_data=["State"])
    st.plotly_chart(fig_default)

    # Trends Over Time
    fig_trend = px.line(filtered_data.groupby("ApprovalFY").size().reset_index(name="Loans"),
                        x="ApprovalFY", y="Loans", title="Loan Trends Over Time")
    st.plotly_chart(fig_trend)

    # Default Rate by Industry
    fig_industry = px.bar(filtered_data.groupby("Industry")["Default"].mean().reset_index(name="Default Rate"), 
                          x="Industry", y="Default Rate", 
                          title="Default Rate by Industry", text_auto=".2f")
    st.plotly_chart(fig_industry)

elif sidebar_option == "Prediction":
    # Prediction Page
    st.title("Loan Default Prediction")
    st.markdown("Enter loan details to predict whether the loan will default.")

    # Creating the form fields
    with st.form("form1", clear_on_submit=False):
        state = st.selectbox("Enter your State", tuple(x['State'].keys()))
        category = st.selectbox("Enter your Bank State", tuple(x['BankState'].keys()))
        appY = st.selectbox("Select your Approval Year", 
                            (1997, 1980, 2006, 1998, 1999, 2000, 2001, 1972, 2003, 2004, 1978,
                             1979, 1981, 2005, 1982, 1983, 1973, 1984, 2007, 1985, 1986, 1987,
                             2008, 1988, 2009, 1989, 1991, 1990, 1974, 2010, 1992, 1993, 2002,
                             1994, 1975, 1977, 1976, 1969, 1995, 1970, 1996, 1971))
        term = st.text_input("Term", "0")
        noemp = st.text_input("Number of Employees", "0")
        urban = st.selectbox("Select the Zone Type", ("Urban", "Rural", "Undefined"))
        rev = st.selectbox("Select Revolving Line of Credit", ("Yes", "No"))
        low = st.selectbox("Select LowDoc Loan Program", ("Yes", "No"))
        disb = st.text_input("Enter the Amount Disbursed", "0")
        merch_long = st.text_input("Enter Gross Amount of Loan Approved by Bank", "0")
        indus = st.selectbox("Enter your Industry Category", tuple(x['Industry'].keys()))
        fran = st.selectbox("Is it a Franchise?", ("Yes", "No"))
        busi = st.selectbox("Is it a New Business?", ("Yes", "No"))
        disY = st.selectbox("Select your Disbursement Year", 
                            (1999, 1997, 1980, 1998, 2006, 2002, 2001, 2000, 2003, 1982, 2004,
                             2071, 2005, 2009, 2007, 2008, 1981, 2072, 1978, 1979, 1996, 2010,
                             1995, 2012, 1983, 1985, 1984, 2048, 1987, 2073, 1986, 2011, 1988,
                             1989, 2013, 1990, 1991, 2014, 1992, 1993, 1994, 2020, 1974, 2028,
                             1975, 1976, 1977, 2069, 2070))
        days_dis = st.text_input("Enter the Days to Disbursement", "0")
        sba = st.text_input("Enter SBA's Guaranteed Amount of Approved Loan", "0")
        appvD = st.selectbox("Is it AppvDisbursed?", ("Yes", "No"))
        realsta = st.selectbox("Is it Real Estate?", ("Yes", "No"))
        great = st.selectbox("During the Great Recession?", ("Yes", "No"))

        # Prepare data for API
        dd = {
            "State": x['State'][state],
            "BankState": x['BankState'][category],
            "ApprovalFY": appY,
            "Term": term,
            "NoEmp": noemp,
            "UrbanRural": urban,
            "RevLineCr": gett(rev),
            "LowDoc": gett(low),
            "DisbursementGross": disb,
            "GrAppv": merch_long,
            "Industry": x['Industry'][indus],
            "IsFranchise": gett(fran),
            "NewBusiness": gett(busi),
            "DisbursementFY": disY,
            "DaysToDisbursement": days_dis,
            "SBA_AppvPct": sba,
            "AppvDisbursed": gett(appvD),
            "RealEstate": gett(realsta),
            "GreatRecession": gett(great),
        }

        submit = st.form_submit_button("Submit this form")
        if submit:
            try:
                res = requests.post("http://127.0.0.1:8000/predict", data=json.dumps(dd))
                predictions = res.json().get("predictions")
                if predictions == [0]:
                    st.success("Paid In Full, The loan was successfully repaid. 😃")
                else:
                    st.error("Charged Off, The loan defaulted and was written off as a loss. 🚨")
            except Exception as e:
                st.error(f"Error: {e}")

    # File uploader for historical transactions
    st.subheader("Or Enter your Historical Transactions CSV File")
    data = st.file_uploader("Choose a CSV File")

    if data is not None:
        try:
            file = {"file": data.getvalue()}
            res = requests.post("http://127.0.0.1:8000/predict/csv", files=file)
            predictions = res.json().get("predictions")
            st.text(predictions)
        except Exception as e:
            st.error(f"Error: {e}")
