import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# 1. Load dataset
df = pd.read_csv("crop_recommendationV2.csv")

print("Original dataset shape:", df.shape)

# 2. Target columns
target_columns = ["N", "P", "K"]

# 3. Separate input features and target values
X = df.drop(columns=target_columns)
y = df[target_columns]

# 4. Identify categorical and numerical columns
categorical_columns = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    exclude=["object", "category"]
).columns.tolist()

print("\nCategorical columns:")
print(categorical_columns)

print("\nNumerical columns:")
print(numerical_columns)

# 5. Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            categorical_columns
        )
    ],
    remainder="passthrough"
)

# 6. Transform input features
X_processed = preprocessor.fit_transform(X)

# 7. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y,
    test_size=0.2,
    random_state=42
)

# 8. Save prepared data
joblib.dump(
    {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "preprocessor": preprocessor
    },
    "prepared_data.pkl"
)

print("\nDataset preparation completed!")
print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)
print("Target shape:", y.shape)

print("\nSaved file: prepared_data.pkl")