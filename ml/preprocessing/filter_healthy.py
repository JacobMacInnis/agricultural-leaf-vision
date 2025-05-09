import os
import shutil
import random
import pandas as pd
from pathlib import Path

# === SETTINGS ===
RAW_DIR = Path("ml/data/raw/leafsnap")
PROCESSED_DIR = Path("ml/data/processed_healthy")
CLEANED_CSV = RAW_DIR / "leafsnap_cleaned.csv"

TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42

# Drop species with very few healthy images (threshold)
DROP_SPECIES_WITH_LESS_THAN = 50  # Change if you want (e.g., 200 if you want stricter)

# Hard drop specific known species
HARDCODED_DROP = {"Squash", "Cotton"}

# === SCRIPT START ===
random.seed(RANDOM_SEED)

# Load cleaned CSV
df = pd.read_csv(CLEANED_CSV)

# Only keep healthy leaves
df = df[df['health'] == 1]

# Drop unwanted species
species_counts = df['name'].value_counts()
species_to_keep = species_counts[species_counts >= DROP_SPECIES_WITH_LESS_THAN].index
species_to_keep = [s for s in species_to_keep if s not in HARDCODED_DROP]

df = df[df['name'].isin(species_to_keep)]

print(f"✅ Keeping {len(species_to_keep)} species: {species_to_keep}")

# Clear and recreate processed_healthy
if PROCESSED_DIR.exists():
    shutil.rmtree(PROCESSED_DIR)
for split in ["train", "val", "test"]:
    (PROCESSED_DIR / split).mkdir(parents=True, exist_ok=True)

# Mapping image_id -> filename
filename_mapping = {}
for file in RAW_DIR.iterdir():
    if file.is_file() and file.name.endswith(".jpg"):
        image_id = int(file.stem.split('_')[0])  # Extract before underscore
        filename_mapping.setdefault(image_id, []).append(file)

# Group by species
species_to_images = {}
for name in df['name'].unique():
    species_df = df[df['name'] == name]
    species_to_images[name] = species_df['id'].tolist()

# Split and copy
for species, image_ids in species_to_images.items():
    random.shuffle(image_ids)
    n_total = len(image_ids)
    n_train = int(n_total * TRAIN_SPLIT)
    n_val = int(n_total * VAL_SPLIT)

    train_ids = image_ids[:n_train]
    val_ids = image_ids[n_train:n_train+n_val]
    test_ids = image_ids[n_train+n_val:]

    for split_name, split_ids in [("train", train_ids), ("val", val_ids), ("test", test_ids)]:
        split_species_dir = PROCESSED_DIR / split_name / species
        split_species_dir.mkdir(parents=True, exist_ok=True)

        for img_id in split_ids:
            matching_files = filename_mapping.get(img_id, [])
            for src_path in matching_files:
                dst_path = split_species_dir / src_path.name
                shutil.copy(src_path, dst_path)

# Summary
counts = []
for split in ["train", "val", "test"]:
    split_dir = PROCESSED_DIR / split
    for species_dir in split_dir.iterdir():
        if species_dir.is_dir():
            n_images = len(list(species_dir.glob("*.jpg")))
            counts.append({"split": split, "species": species_dir.name, "count": n_images})

df_counts = pd.DataFrame(counts)
df_counts.to_csv(PROCESSED_DIR / "split_summary.csv", index=False)

print("✅ Dataset filtering + splitting complete.")
print(df_counts.pivot(index="species", columns="split", values="count").fillna(0))
