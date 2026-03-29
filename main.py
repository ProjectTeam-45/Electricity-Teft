from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load trained model
model = joblib.load("electricity_theft_model.pkl")


@app.get("/")
def home():
    return {"message": "Electricity Theft Detection API running"}


@app.post("/predict")
def predict(data: dict):

    # 🔁 Map input → training features
    input_data = {
        "mtr_tariff": data["tarif_type"],
        "mtr_id": data["counter_number"],
        "mtr_status": data["counter_statue"],
        "mtr_code": data["counter_code"],
        "mtr_notes": data["reading_remarque"],
        "mtr_coef": data["counter_coefficient"],

        "usage_1": data["consommation_level_1"],
        "usage_2": data["consommation_level_2"],
        "usage_3": data["consommation_level_3"],
        "usage_4": data["consommation_level_4"],

        "mtr_val_old": data["old_index"],
        "mtr_val_new": data["new_index"],
        "months_num": data["months_number"],

        "mtr_type": data["counter_type"],

        # Default / missing fields
        "usage_aux": 0,
        "usage_n_aux": 0,
        "date_flip_flag": 0,
        "date_overlap_invoice": 0,
        "date_overlap_months": 0,

        "months_num_calc": data["months_number"],
        "R_1": 0,
        "R_2a": 0,
        "R_2b": 0,
        "R_3a": 0,
        "R_3b": 0,

        "idx": 0,
        "idx_prv": -1,
        "idx_nxt": -1,

        "year": data["invoice_year"],
        "month": data["invoice_month"]
    }

    input_df = pd.DataFrame([input_data])

    # 🔮 Prediction
    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    # 📊 Rule-based detection
    meter_difference = data["new_index"] - data["old_index"]
    total_consumption = (
        data["consommation_level_1"]
        + data["consommation_level_2"]
        + data["consommation_level_3"]
        + data["consommation_level_4"]
    )

    fraud_type = "Normal Consumption"

    if meter_difference > 10000 and total_consumption < 50:
        prediction = 1
        probability = 0.95
        fraud_type = "Meter Bypassing Detected"

    return {
        "prediction": prediction,
        "theft_probability": probability,
        "fraud_type": fraud_type
    }
