import streamlit as st
import requests

API_URL = "https://cropai-project.onrender.com"

st.set_page_config(page_title="Crop AI Dashboard", layout="wide")

st.title("🌾 Crop AI – Disease Detection & Recommendations")


# -----------------------------
# Disease Detection Section
# -----------------------------
st.header("🩺 Crop Disease Detection")

uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.image(uploaded_file, caption="Uploaded leaf image", use_column_width=True)

    if st.button("Predict Disease"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        with st.spinner("Predicting disease..."):
            try:
                resp = requests.post(f"{API_URL}/predict-disease", files=files)

                if resp.status_code == 200:
                    data = resp.json()
                    label = data["disease_label"]
                    conf = data["confidence"]

                    # Confidence-based message
                    if conf < 0.60:
                        st.warning(
                        f"⚠️ Model is not confident.\n\n"
                        f"Predicted: **{label}**\n"
                        f"Confidence: **{conf:.2f}**"
                    )
                    else:
                        st.success(f"Disease: {label}")
                        st.write(f"Confidence: {conf:.2f}")

                else:
                    st.error(f"Error: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")


st.markdown("---")

# -----------------------------
# Crop Recommendation Section
# -----------------------------
st.header("🌱 Crop Recommendation")

with st.form("crop_form"):
    N = st.number_input("Nitrogen (N)", value=90.0)
    P = st.number_input("Phosphorus (P)", value=42.0)
    K = st.number_input("Potassium (K)", value=43.0)
    temperature = st.number_input("Temperature (°C)", value=22.0)
    humidity = st.number_input("Humidity (%)", value=80.0)
    ph = st.number_input("pH", value=6.5)
    rainfall = st.number_input("Rainfall (mm)", value=200.0)

    submit_crop = st.form_submit_button("Recommend Crop")

if submit_crop:
    payload = {
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }
    with st.spinner("Getting crop recommendation..."):
        try:
            resp = requests.post(f"{API_URL}/recommend-crop", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                st.success(f"Recommended Crop: {data['recommended_crop']}")
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")


st.markdown("---")

# -----------------------------
# Fertilizer Recommendation Section
# -----------------------------
st.header("💧 Fertilizer Recommendation")

with st.form("fert_form"):
    Temparature = st.number_input("Temperature (°C)", value=26.0)
    Humidity = st.number_input("Humidity (%)", value=52.0)
    Moisture = st.number_input("Moisture", value=38.0)

    Soil_Type = st.text_input("Soil Type (exact as in dataset, e.g. 'Loamy')")
    Crop_Type = st.text_input("Crop Type (exact as in dataset, e.g. 'Sugarcane')")

    Nitrogen = st.number_input("Nitrogen", value=50.0)
    Potassium = st.number_input("Potassium", value=40.0)
    Phosphorous = st.number_input("Phosphorous", value=40.0)

    submit_fert = st.form_submit_button("Recommend Fertilizer")

if submit_fert:
    payload = {
        "Temparature": Temparature,
        "Humidity": Humidity,
        "Moisture": Moisture,
        "Soil_Type": Soil_Type,
        "Crop_Type": Crop_Type,
        "Nitrogen": Nitrogen,
        "Potassium": Potassium,
        "Phosphorous": Phosphorous
    }
    with st.spinner("Getting fertilizer recommendation..."):
        try:
            resp = requests.post(f"{API_URL}/recommend-fertilizer", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                st.success(f"Recommended Fertilizer: {data['recommended_fertilizer']}")
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
