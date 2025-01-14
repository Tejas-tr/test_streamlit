import streamlit as st
import pandas as pd
import pickle
import joblib

st.title('Car Price prediction App')

target_encode = joblib.load('target_encoder.joblib')

# Define our encoding dictionary
encode_dict = {
    "fuel_type": {
        "Diesel": 1, 
        "Petrol": 2, 
        "CNG": 3, 
        "LPG": 4, 
        "Electric": 5
    },
    "transmission_type": {
        "Manual": 1, 
        "Automatic": 2
    },
    "seller_type": {
        "Dealer": 1, 
        "Individual": 2, 
        "Trustmark Dealer": 3
    }
}

#df['fuel_type'] = target_encode.fit_transform(df['fuel_type'], df['selling_price'])
#df['transmission_type'] = target_encode.fit_transform(df['transmission_type'], df['selling_price'])
#df['seller_type'] = target_encode.fit_transform(df['seller_type'], df['selling_price'])

model = pickle.load(open("cars24-model.pkl", "rb"))

st.subheader("Please fill in the details below:")
year = st.slider("Manufacturing Year", min_value=1990, max_value=2025, value=2018, step=1)
seller_type = st.selectbox("Seller Type", list(encode_dict["seller_type"].keys()))
km_driven = st.number_input("Kilometers Driven", min_value=0, value=40000, step=5000)
fuel_type = st.selectbox("fuel_type", list(encode_dict["fuel_type"].keys()))
transmission_type = st.radio("Transmission Type", list(encode_dict["transmission_type"].keys()))
mileage = st.number_input("Mileage (kmpl)", min_value=0.0, value=18.0, step=0.5)
engine = st.number_input("Engine (CC)", min_value=500, max_value=5000, value=1200, step=100)
max_power = st.number_input("Max Power (bhp)", min_value=50.0, max_value=500.0, value=85.0, step=5.0)
seats = st.selectbox("Seats", [2, 4, 5, 6, 7, 8, 9, 10])

def model_pred(
    year, seller_type, km_driven, fuel_type, 
    transmission_type, mileage, engine, max_power, seats
):
	# Convert categorical features using the encode dictionary
    df = pd.DataFrame({ 'fuel_type': [fuel_type], 'transmission_type': [transmission_type], 'seller_type': [seller_type] })
    
    df[['fuel_type', 'transmission_type', 'seller_type']] = target_encode.transform(df[['fuel_type', 'transmission_type', 'seller_type']])
    #fuel_type_enc = target_encode.transform(fuel_type)
    #transmission_type_enc = target_encode.transform(transmission_type)
    #st.write(df)
    fuel_type_enc = df['fuel_type']
    transmission_type_enc = df['transmission_type']
    seller_type_enc = df['seller_type']

    
	# Ensure numeric features are floats or ints as needed
    data = [[
        float(year),
        float(seller_type_enc[0]),
        float(km_driven),
        float(fuel_type_enc[0]),
        float(transmission_type_enc[0]),
        float(mileage),
        float(engine),
        float(max_power),
        float(seats)
    ]]

    scaler = joblib.load('scaler.joblib')
    # Scale the data
    data = scaler.transform(data)
        
	# Predict
    prediction = model.predict(data)
    return round(prediction[0], 2)

if st.button("Predict"):
    price = model_pred(
        year, seller_type, km_driven, 
        fuel_type, transmission_type, 
        mileage, engine, max_power, seats
    )
    st.write(f"**Predicted Car Price**: {price} Lakhs (approx.)")
else:
    st.write("Click the **Predict** button once you've entered all the details.")
