# import pandas as pd
# from datasets import load_dataset

# # Load dataset
# dataset = load_dataset("yusuf802/leaf-images", split="train")
# label_names = dataset.features["label"].names

# # Build initial dataframe
# filenames = [f"{i}.jpg" for i in range(len(dataset))]
# species = [label_names[item['label']] for item in dataset]

# df = pd.DataFrame({
#     "filename": filenames,
#     "species": species
# })

# # Now clean it
# def extract_name(species_label):
#     # Remove everything after the first underscore
#     return species_label.split('_')[0]

# def determine_health(species_label):
#     # If 'healthy' is anywhere in the label, mark as healthy
#     return 1 if 'healthy' in species_label.lower() else 0

# df['id'] = df['filename'].str.replace('.jpg', '').astype(int)
# df['name'] = df['species'].apply(extract_name)
# df['health'] = df['species'].apply(determine_health)

# # Final clean DataFrame
# final_df = df[['id', 'name', 'health']]

# # Save cleaned CSV
# output_path = "data/raw/leafsnap/leafsnap_cleaned.csv"
# final_df.to_csv(output_path, index=False)

# print(f"✅ Cleaned CSV saved to {output_path}")


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

