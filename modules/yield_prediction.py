import joblib
import pandas as pd


MODEL_PATH = "models/yield_model.pkl"


# Load trained model
model = joblib.load(MODEL_PATH)


def predict_yield(
    soil_ph,
    soil_moisture,
    avg_temperature,
    total_rainfall,
    fertilizer_amount,
    pesticide_usage,
    sunlight_hours,
    nitrogen_content,
    phosphorus_content,
    potassium_content,
    irrigation_frequency,
    crop_type,
    region,
    season,
    harvest_year,
    harvest_month
):

    data = pd.DataFrame([
        {
            "soil_ph": soil_ph,
            "soil_moisture": soil_moisture,
            "avg_temperature": avg_temperature,
            "total_rainfall": total_rainfall,
            "fertilizer_amount": fertilizer_amount,
            "pesticide_usage": pesticide_usage,
            "sunlight_hours": sunlight_hours,
            "nitrogen_content": nitrogen_content,
            "phosphorus_content": phosphorus_content,
            "potassium_content": potassium_content,
            "irrigation_frequency": irrigation_frequency,
            "crop_type": crop_type,
            "region": region,
            "season": season,
            "harvest_year": harvest_year,
            "harvest_month": harvest_month
        }
    ])

    prediction = model.predict(data)

    return prediction[0]