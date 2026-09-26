import joblib
import numpy as np

# Load trained model
model = joblib.load("soil_model.pkl")

print("\n🌱 SoilSense AI")
print("-----------------------")
print("Enter Soil Details")

# Get user input
ph = float(input("Enter pH: "))
moisture = float(input("Enter Soil Moisture: "))
temperature = float(input("Enter Temperature: "))
humidity = float(input("Enter Humidity: "))
organic_matter = float(input("Enter Organic Matter: "))
soil_type = float(input("Enter Soil Type (encoded number): "))

# Prepare input
soil_data = np.array([[
    ph,
    moisture,
    temperature,
    humidity,
    organic_matter,
    soil_type
]])

# Predict NPK
prediction = model.predict(soil_data)

print("\n-----------------------")
print("🌱 SoilSense AI Result")
print("-----------------------")

print("Predicted Nitrogen (N):", prediction[0][0])
print("Predicted Phosphorus (P):", prediction[0][1])
print("Predicted Potassium (K):", prediction[0][2])
