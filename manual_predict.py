import joblib
import pandas as pd

# Load trained model
model = joblib.load("soil_model.pkl")

# Load saved data
data = joblib.load("data.pkl")

preprocessor = data.get("preprocessor")

# Check preprocessor
if preprocessor is None:
    print("Error: Preprocessor is missing!")
    print("Please save the preprocessor during data preparation.")
    exit()

# Load original dataset
df = pd.read_csv("Crop_recommendationV2.csv")

# Use first row as base
sample = df.iloc[[0]].copy()

print("\n🌱 SoilSense AI - Manual Input")

# Get user inputs
temperature = float(input("Enter Temperature: "))
humidity = float(input("Enter Humidity: "))
ph = float(input("Enter pH: "))
soil_moisture = float(input("Enter Soil Moisture: "))
organic_matter = float(input("Enter Organic Matter: "))


# Update soil values
sample["temperature"] = temperature
sample["humidity"] = humidity
sample["ph"] = ph
sample["soil_moisture"] = soil_moisture
sample["organic_matter"] = organic_matter

# Remove target columns if present
target_columns = ["N", "P", "K", "nitrogen", "phosphorus", "potassium"]

sample = sample.drop(
    columns=[col for col in target_columns if col in sample.columns],
    errors="ignore"
)

# Transform input
processed_sample = preprocessor.transform(sample)

# Predict NPK
prediction = model.predict(processed_sample)

print("\n-----------------------------")
print("🌱 SoilSense AI Result")
print("-----------------------------")

print("Predicted Nitrogen (N):", prediction[0][0])
print("Predicted Phosphorus (P):", prediction[0][1])
print("Predicted Potassium (K):", prediction[0][2])

print("\nManual prediction completed!")