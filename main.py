from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("electricity_theft_model.pkl")

features = [
"tarif_type","counter_number","counter_statue","counter_code",
"reading_remarque","counter_coefficient",
"consommation_level_1","consommation_level_2","consommation_level_3",
"consommation_level_4","old_index","new_index","months_number",
"counter_type","disrict","client_catg","region",
"invoice_year","invoice_month","client_year"
]


@app.get("/")
def home():
    return {"message":"Electricity Theft Detection API running"}


@app.post("/predict")
def predict(data: dict):

    input_df = pd.DataFrame([data], columns=features)

    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    return {
        "prediction": prediction,
        "theft_probability": probability
    }