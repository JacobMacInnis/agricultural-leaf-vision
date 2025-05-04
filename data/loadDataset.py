from datasets import load_dataset
import os
import shutil

# Step 1: Load the dataset from HuggingFace
dataset = load_dataset("yusuf802/leaf-images", split="train")

# Step 2: Define target directory
target_dir = "data/leafsnap"

# Step 3: Create the target folder if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Step 4: Save images and CSV metadata manually
for idx, item in enumerate(dataset):
    image = item["image"]
    label = item["label"]

    # Save image
    img_path = os.path.join(target_dir, f"{idx}_{label}.jpg")
    image.save(img_path)

print(f"Saved {len(dataset)} images to {target_dir}")
