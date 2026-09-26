import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("crop_recommendationV2.csv")

# Input features
X = df[["N", "P", "K"]]

# Target column
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Crop Model Trained Successfully!")
print("Accuracy:", round(accuracy * 100, 2), "%")

# Save model
joblib.dump(model, "crop_model.pkl")

print("crop_model.pkl saved successfully!") 