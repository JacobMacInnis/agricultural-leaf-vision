import random
import shutil
from pathlib import Path

# Settings
INPUT_DIR = Path("ml/data/processed_healthy")  # Your current dataset
OUTPUT_DIR = Path("ml/data/processed_balanced")
TARGET_COUNT = 400  # Images per class after balancing
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

# Make output folders
for split in ["train", "val", "test"]:
    (OUTPUT_DIR / split).mkdir(parents=True, exist_ok=True)

# Copy balanced dataset
for split in ["train", "val", "test"]:
    input_split = INPUT_DIR / split
    output_split = OUTPUT_DIR / split

    for species_dir in input_split.iterdir():
        if species_dir.is_dir():
            images = list(species_dir.glob("*.jpg"))
            if len(images) >= TARGET_COUNT:
                selected_images = random.sample(images, TARGET_COUNT)
            else:
                selected_images = images  # If not enough, take all

            output_species_dir = output_split / species_dir.name
            output_species_dir.mkdir(parents=True, exist_ok=True)

            for img_path in selected_images:
                shutil.copy(img_path, output_species_dir / img_path.name)

print("✅ Dataset balanced and saved to:", OUTPUT_DIR)
