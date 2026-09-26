import joblib

# Load prepared data
data = joblib.load("prepared_data.pkl")

print("\nData Keys:")
print(data.keys())

print("\nFeature Information:")

X_train = data["X_train"]

print("Number of features:", X_train.shape[1])

print("\nFeature Names:")

if hasattr(X_train, "columns"):
    print(list(X_train.columns))
else:
    print("Feature names are not available.")