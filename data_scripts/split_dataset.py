import os
import random
import shutil
from collections import defaultdict

# Configuration
RAW_DIR = "data/raw/leafsnap/"
PROCESSED_DIR = "data/processed/"
NUM_SPECIES_TO_SELECT = 15  # You can change this
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

# Step 1: Group images by species
species_to_images = defaultdict(list)

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".jpg"):
        try:
            idx, species = filename.split("_")
            species = species.replace(".jpg", "").strip()
            species_to_images[species].append(filename)
        except ValueError:
            print(f"Skipping file: {filename}")

# Step 2: Pick random species
all_species = list(species_to_images.keys())
selected_species = random.sample(all_species, NUM_SPECIES_TO_SELECT)

print(f"Selected species ({len(selected_species)}): {selected_species}")

# Step 3: Create folders
for split in ["train", "val", "test"]:
    for species in selected_species:
        os.makedirs(os.path.join(PROCESSED_DIR, split, species), exist_ok=True)

# Step 4: Split images into train/val/test
for species in selected_species:
    images = species_to_images[species]
    random.shuffle(images)

    train_cutoff = int(len(images) * TRAIN_SPLIT)
    val_cutoff = int(len(images) * (TRAIN_SPLIT + VAL_SPLIT))

    train_images = images[:train_cutoff]
    val_images = images[train_cutoff:val_cutoff]
    test_images = images[val_cutoff:]

    for split_name, split_images in zip(["train", "val", "test"], [train_images, val_images, test_images]):
        for img in split_images:
            src_path = os.path.join(RAW_DIR, img)
            dest_path = os.path.join(PROCESSED_DIR, split_name, species, img)
            shutil.copy(src_path, dest_path)

print("✅ Dataset split and saved successfully!")
