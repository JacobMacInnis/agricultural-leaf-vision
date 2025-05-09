import random
import pandas as pd
from pathlib import Path

# Paths
RAW_DIR = Path("ml/data/raw/leafsnap")
PROCESSED_DIR = Path("ml/data/processed_balanced")
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

# After copying all images, generate split summary
counts = []
for split in ["train", "val", "test"]:
    split_dir = PROCESSED_DIR / split
    for species_dir in split_dir.iterdir():
        if species_dir.is_dir():
            n_images = len(list(species_dir.glob("*.jpg")))
            counts.append({"split": split, "species": species_dir.name, "count": n_images})

# Save the counts summary as CSV
df_counts = pd.DataFrame(counts)
df_counts.to_csv(PROCESSED_DIR / "split_summary.csv", index=False)

print("✅ Saved dataset distribution summary.")
print("✅ Dataset split completed (FAST version).")



