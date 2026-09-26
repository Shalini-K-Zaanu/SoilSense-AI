import pandas as pd

# Read the dataset
file_path = "crop_recommendationV2.csv"

df = pd.read_csv(file_path)

print("DATASET LOADED SUCCESSFULLY")
print("=" * 40)

# Display number of rows and columns
print("Dataset shape:", df.shape)

# Display column names
print("\nColumn names:")
print(df.columns.tolist())

# Display first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Display data types
print("\nData types:")
print(df.dtypes)

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())