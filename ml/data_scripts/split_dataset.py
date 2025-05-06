import os
import shutil
import random
import pandas as pd
from pathlib import Path

# Paths
RAW_DIR = Path("data/raw/leafsnap")
PROCESSED_DIR = Path("data/processed")
CLEANED_CSV = RAW_DIR / "leafsnap_cleaned.csv"

# Settings
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42

# Set random seed
random.seed(RANDOM_SEED)

# Read cleaned CSV
df = pd.read_csv(CLEANED_CSV)

# Create directories
for split in ["train", "val", "test"]:
    split_dir = PROCESSED_DIR / split
    if split_dir.exists():
        shutil.rmtree(split_dir)
    split_dir.mkdir(parents=True, exist_ok=True)

# Build a mapping of image_id -> full path
filename_mapping = {}
for file in RAW_DIR.iterdir():
    if file.is_file() and file.name.endswith(".jpg"):
        base_name = file.stem  # Get filename without .jpg
        if '_' in base_name:
            image_id = int(base_name.split('_')[0])  # Take part before underscore
            filename_mapping.setdefault(image_id, []).append(file)

# Group by plant name
species_to_images = {}
for name in df['name'].unique():
    species_df = df[df['name'] == name]
    species_to_images[name] = species_df['id'].tolist()

# Split and copy images
for species, image_ids in species_to_images.items():
    random.shuffle(image_ids)
    n_total = len(image_ids)
    n_train = int(n_total * TRAIN_SPLIT)
    n_val = int(n_total * VAL_SPLIT)

    train_ids = image_ids[:n_train]
    val_ids = image_ids[n_train:n_train + n_val]
    test_ids = image_ids[n_train + n_val:]

    for split_name, split_ids in [("train", train_ids), ("val", val_ids), ("test", test_ids)]:
        split_species_dir = PROCESSED_DIR / split_name / species
        split_species_dir.mkdir(parents=True, exist_ok=True)

        for img_id in split_ids:
            matching_files = filename_mapping.get(img_id, [])
            if matching_files:
                for src_path in matching_files:
                    dst_path = split_species_dir / src_path.name
                    shutil.copy(src_path, dst_path)
            else:
                print(f"Warning: No matching file found for ID {img_id}")

print("✅ Dataset split completed (FAST version).")
