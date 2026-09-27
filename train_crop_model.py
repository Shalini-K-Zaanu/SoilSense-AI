import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("Crop_recommendationV2.csv")

# Use all features except crop label
X = df.drop(columns=["label"])
y = df["label"]

print("--------------------------------")
print("SoilSense AI Crop Model")
print("--------------------------------")

print("Total crops:", y.nunique())
print("Total features:", X.shape[1])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    max_depth=None,
    min_samples_leaf=1
)

print("Training crop model...")

model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("--------------------------------")
print("Crop Model Training Completed")
print("--------------------------------")

print("Accuracy:", round(accuracy * 100, 2), "%")
print("Classes learned:", len(model.classes_))

# Save model
joblib.dump(
    model,
    "crop_model.pkl"
)

print("--------------------------------")
print("crop_model.pkl saved successfully!")
print("--------------------------------")