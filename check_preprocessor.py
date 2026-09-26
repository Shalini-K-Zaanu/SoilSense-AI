import joblib

# Load prepared data
data = joblib.load("prepared_data.pkl")

# Get preprocessor
preprocessor = data["preprocessor"]

print("\nPreprocessor Details")
print("-----------------------")

print(preprocessor)

print("\nTransformer Information:")

for name, transformer, columns in preprocessor.transformers_:
    print("\nName:", name)
    print("Columns:", columns)
    print("Transformer:", transformer)

    if hasattr(transformer, "categories_"):
        print("Categories:", transformer.categories_)