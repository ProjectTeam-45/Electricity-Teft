import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Electricity Theft Detection", layout="centered")

st.title("⚡ Electricity Theft Detection Dashboard")
st.write("Enter electricity consumption data to detect possible theft.")

col1, col2 = st.columns(2)

with col1:
    consommation_level_1 = st.slider("Consumption Level 1",0,1000,120)
    consommation_level_2 = st.slider("Consumption Level 2",0,1000,50)
    old_index = st.number_input("Previous Meter Reading",0,100000,14000)
    months_number = st.slider("Billing Months",1,12,4)

with col2:
    consommation_level_3 = st.slider("Consumption Level 3",0,1000,0)
    consommation_level_4 = st.slider("Consumption Level 4",0,1000,0)
    new_index = st.number_input("Current Meter Reading",0,100000,14200)
    region = st.slider("Region Code",0,500,101)

api_url = "https://electricity-theft-api.onrender.com/predict"

if st.button("Predict Theft"):

    data = {
        "tarif_type":11,
        "counter_number":1335667,
        "counter_statue":0,
        "counter_code":203,
        "reading_remarque":8,
        "counter_coefficient":1,
        "consommation_level_1":consommation_level_1,
        "consommation_level_2":consommation_level_2,
        "consommation_level_3":consommation_level_3,
        "consommation_level_4":consommation_level_4,
        "old_index":old_index,
        "new_index":new_index,
        "months_number":months_number,
        "counter_type":1,
        "disrict":60,
        "client_catg":11,
        "region":region,
        "invoice_year":datetime.now().year,
        "invoice_month":datetime.now().month,
        "client_year":1994
    }

    with st.spinner("Analyzing electricity consumption..."):
        response = requests.post(api_url,json=data)
        result = response.json()

    prediction = result["prediction"]
    probability = result["theft_probability"]

    if prediction == 1:
        st.error(f"⚠️ Theft Suspected (Probability {probability:.2f})")
    else:
        st.success(f"✅ Normal Consumption (Probability {probability:.2f})")

    prob_percent = probability*100

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_percent,
        title={'text':"Theft Probability (%)"},
        gauge={
            'axis':{'range':[0,100]},
            'steps':[
                {'range':[0,40],'color':"green"},
                {'range':[40,70],'color':"yellow"},
                {'range':[70,100],'color':"red"}
            ]
        }
    ))

    st.plotly_chart(fig)
