import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("data/raw/leafsnap/leafsnap_cleaned.csv")

# 1. See how many unique plant types there are
unique_plants = df['name'].nunique()
print(f"✅ Number of unique plant types: {unique_plants}")

# 2. (Optional) See what all the unique plant names are
plant_names = df['name'].unique()
print(f"✅ Plant types:\n{plant_names}")
