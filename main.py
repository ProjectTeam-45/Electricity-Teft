from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load trained model
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
    return {"message": "Electricity Theft Detection API running"}


@app.post("/predict")
def predict(data: dict):

    # Convert input to dataframe
    input_df = pd.DataFrame([data], columns=features)

    # Model prediction
    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    # Calculate values for rule detection
    meter_difference = data["new_index"] - data["old_index"]
    total_consumption = (
        data["consommation_level_1"]
        + data["consommation_level_2"]
        + data["consommation_level_3"]
        + data["consommation_level_4"]
    )

    fraud_type = "Normal Consumption"

    # Rule-based detection for meter bypassing
    if meter_difference > 10000 and total_consumption < 50:
        prediction = 1
        probability = 0.95
        fraud_type = "Meter Bypassing Detected"

    return {
        "prediction": prediction,
        "theft_probability": probability,
        "fraud_type": fraud_type
    }
