import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load prepared data
data = joblib.load("prepared_data.pkl")

X_train = data["X_train"]
X_test = data["X_test"]
y_train = data["y_train"]
y_test = data["y_test"]

# Load preprocessor
preprocessor = data.get("preprocessor", None)

print("Prepared data loaded successfully!")

# Create model
model = LinearRegression()

# Train the model
print("Training model...")

model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel training completed!")
print("Mean Absolute Error:", mae)
print("R2 Score:", r2)

# Save trained model
joblib.dump(model, "soil_model.pkl")

# Save test data and preprocessor
test_data = {
    "X_test": X_test,
    "y_test": y_test,
    "preprocessor": preprocessor
}

joblib.dump(test_data, "data.pkl")

print("\nSaved files:")
print("soil_model.pkl")
print("data.pkl")