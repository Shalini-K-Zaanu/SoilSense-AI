import pickle
import joblib
import numpy as np

# Load trained model
model = joblib.load("soil_model.pkl")

# Load prepared data
with open("data.pkl", "rb") as file:
    data = pickle.load(file)

X_test = data["x_test"]
y_test = data["y_test"]

# Take one test sample
if hasattr(X_test, "iloc"):
    sample = X_test.iloc[[0]]
    actual = y_test.iloc[0] if hasattr(y_test, "iloc") else y_test[0]
else:
    sample = np.asarray(X_test)[0].reshape(1, -1)
    actual = np.asarray(y_test)[0]

# Predict NPK
prediction = model.predict(sample)

print("\n-----------------------------")
print("🌱 SoilSense AI Result")
print("-----------------------------")

print("Predicted NPK:", prediction[0])
print("Actual NPK:", actual)

print("\nPrediction completed successfully!")