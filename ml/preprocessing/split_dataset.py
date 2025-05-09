import pandas as pd
import shutil
from pathlib import Path

# === Paths ===
RAW_CSV = Path("ml/data/raw/leafsnap/leafsnap_cleaned.csv")
RAW_DIR = Path("ml/data/raw/leafsnap")
PROCESSED_DIR = Path("ml/data/processed_healthy")

# === Settings ===
HARDCODED_DROP = {"Squash", "Cotton", "Potato", "Wheat", "Orange"}
HEALTHY_ONLY = True

# === Read cleaned CSV ===
df = pd.read_csv(RAW_CSV)

# === Apply filtering ===
if HEALTHY_ONLY:
    df = df[df["health"] == 1]

df = df[~df["name"].isin(HARDCODED_DROP)]  # Drop unwanted species
print(f"✅ After filtering, dataset has {len(df)} samples and {df['name'].nunique()} species.")
print(f"Classes: {sorted(df['name'].unique())}")

# === Create new processed_healthy directory structure ===
for split in ["train", "val", "test"]:
    split_dir = PROCESSED_DIR / split
    if split_dir.exists():
        shutil.rmtree(split_dir)
    split_dir.mkdir(parents=True, exist_ok=True)

# === (Optional) Split into train/val/test ===
# (You can keep using your existing split_dataset.py or reimplement here if needed.)

# Mapping image_id to file
filename_mapping = {}
for file in RAW_DIR.iterdir():
    if file.is_file() and file.name.endswith(".jpg"):
        base_name = file.stem
        if '_' in base_name:
            image_id = int(base_name.split('_')[0])
            filename_mapping.setdefault(image_id, []).append(file)

# Group by species
species_to_images = {}
for name in df['name'].unique():
    species_df = df[df['name'] == name]
    species_to_images[name] = species_df['id'].tolist()

# Train/val/test split ratios
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42

import random
random.seed(RANDOM_SEED)

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
            if matching_files:
                for src_path in matching_files:
                    dst_path = split_species_dir / src_path.name
                    shutil.copy(src_path, dst_path)
            else:
                print(f"Warning: No matching file found for ID {img_id}")

print("✅ Healthy dataset created and split!")

# === (Optional) Save counts to CSV to verify ===
counts = []
for split in ["train", "val", "test"]:
    split_dir = PROCESSED_DIR / split
    for species_dir in split_dir.iterdir():
        if species_dir.is_dir():
            n_images = len(list(species_dir.glob("*.jpg")))
            counts.append({"split": split, "species": species_dir.name, "count": n_images})

df_counts = pd.DataFrame(counts)
df_counts.to_csv(PROCESSED_DIR / "split_summary.csv", index=False)

print("✅ Split summary saved!")
