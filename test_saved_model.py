import joblib

# Load trained model
model = joblib.load("soil_model.pkl")

# Load test data
data = joblib.load("data.pkl")

X_test = data["X_test"]
y_test = data["y_test"]

# Select one test sample
sample = X_test[0:1]

# Predict NPK
prediction = model.predict(sample)

print("\n-----------------------------")
print("🌱 SoilSense AI Result")
print("-----------------------------")

print("Predicted NPK:", prediction[0])
print("Actual NPK:", y_test.iloc[0] if hasattr(y_test, "iloc") else y_test[0])

print("\nModel testing completed successfully!")