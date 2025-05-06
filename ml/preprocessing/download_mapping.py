import pandas as pd

# Load the local CSV you already have
input_path = "data/raw/leafsnap/leafsnap_mapping.csv"
df = pd.read_csv(input_path)

# Cleaning functions
def extract_name(species_label):
    # Plant name before first underscore
    return species_label.split('_')[0]

def determine_health(species_label):
    # 1 if healthy, 0 otherwise
    return 1 if 'healthy' in species_label.lower() else 0

def extract_disease(species_label):
    # If healthy, return 'none', otherwise extract disease name after first underscore
    if 'healthy' in species_label.lower():
        return 'none'
    parts = species_label.split('_')
    return '_'.join(parts[1:]) if len(parts) > 1 else 'unknown'

# Create new columns
df['id'] = df['filename'].str.replace('.jpg', '').astype(int)
df['name'] = df['species'].apply(extract_name)
df['health'] = df['species'].apply(determine_health)
df['disease'] = df['species'].apply(extract_disease)

# Final cleaned DataFrame
final_df = df[['id', 'name', 'health', 'disease']]

# Save to new cleaned CSV
output_path = "data/raw/leafsnap/leafsnap_cleaned.csv"
final_df.to_csv(output_path, index=False)

print(f"✅ Cleaned CSV with disease info saved to {output_path}")

