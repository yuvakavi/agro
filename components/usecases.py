import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
from keras.models import load_model
from keras.preprocessing import image

# === Define base path (inside components/) ===
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")

# === Load Models & Data ===
crop_model = joblib.load(os.path.join(MODELS_DIR, "crop_model.joblib"))
disease_model = load_model(os.path.join(MODELS_DIR, "crop_disease_model.h5"))
treatment_df = pd.read_csv(os.path.join(MODELS_DIR, "crop_disease_treatment.csv"))
rf_model = joblib.load(os.path.join(MODELS_DIR, "rf_model_latest.pkl"))
label_encoders = joblib.load(os.path.join(MODELS_DIR, "label_encoders.pkl"))
advisor_df = pd.read_csv(os.path.join(MODELS_DIR, "crop_advisor_download.csv"))

# === Use Case 1: Crop Recommendation ===
def crop_recommendation_ui():
    st.header("🌱 Crop Recommendation")
    N = st.number_input("Nitrogen", 0)
    P = st.number_input("Phosphorus", 0)
    K = st.number_input("Potassium", 0)
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    ph = st.number_input("pH level")
    rainfall = st.number_input("Rainfall (mm)")

    if st.button("🔍 Recommend Crop"):
        data = [[N, P, K, temperature, humidity, ph, rainfall]]
        prediction = crop_model.predict(data)[0]
        st.success(f"✅ Recommended Crop: {prediction}")

# === Use Case 2: Crop Disease Detection ===
def disease_detection_ui():
    st.header("🦠 Crop Disease Detection")
    uploaded_file = st.file_uploader("Upload leaf image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = image.load_img(uploaded_file, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = disease_model.predict(img_array)
        predicted_index = np.argmax(prediction)
        class_names = sorted(treatment_df["label"].unique())
        predicted_class = class_names[predicted_index]

        treatment_map = dict(zip(treatment_df["label"], treatment_df["treatment"]))
        treatment = treatment_map.get(predicted_class, "⚠️ No treatment info available.")

        st.image(img, caption="Uploaded Image", use_column_width=True)
        st.subheader(f"🦠 Detected Disease: {predicted_class}")
        st.info(f"💊 Suggested Treatment: {treatment}")

# === Use Case 3: Market Price Analysis ===
def market_price_ui():
    st.header("📈 Market Price Prediction")
    state = st.text_input("State")
    district = st.text_input("District")
    market = st.text_input("Market")
    commodity = st.text_input("Commodity")
    variety = st.text_input("Variety")
    min_price = st.number_input("Min Price")
    max_price = st.number_input("Max Price")
    year = st.number_input("Year", value=2025)
    month = st.number_input("Month", min_value=1, max_value=12)

    if st.button("🔍 Predict Price"):
        data = {
            'State': state, 'District': district, 'Market': market,
            'Commodity': commodity, 'Variety': variety,
            'Min_Price': min_price, 'Max_Price': max_price,
            'year': year, 'month': month,
            'Rainfall_mm': 150,
            'Demand_Index': 1.0,
            'Nearby_Market_Avg_Price': (min_price + max_price) / 2,
            'Price_Volatility': 100,
            'Price_MA': (min_price + max_price) / 2
        }

        for col in ['State', 'District', 'Market', 'Commodity', 'Variety']:
            if data[col] in label_encoders[col].classes_:
                data[col] = label_encoders[col].transform([data[col]])[0]
            else:
                data[col] = 0

        input_df = pd.DataFrame([data])
        prediction = rf_model.predict(input_df)[0]
        st.success(f"💰 Predicted Modal Price: ₹{prediction:.2f}")

# === Use Case 4: Crop Advisory ===
def advisor_ui():
    st.header("📘 Crop Advisory")
    crop_name = st.text_input("Enter crop name")

    if st.button("🔍 Get Advice"):
        crop_col = [col for col in advisor_df.columns if 'crop' in col.lower()][0]
        crop_data = advisor_df[advisor_df[crop_col].str.lower() == crop_name.lower()]

        if crop_data.empty:
            st.warning(f"❌ No data found for '{crop_name}'.")
        else:
            st.subheader(f"🌾 Advisory for {crop_name.title()}")
            for col in crop_data.columns:
                if col != crop_col:
                    st.write(f"🔹 {col}: {crop_data.iloc[0][col]}")






