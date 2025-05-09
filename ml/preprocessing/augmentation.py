import tensorflow as tf
import os
from pathlib import Path
from tqdm import tqdm

# Settings
INPUT_DIR = Path("ml/data/processed_balanced")
OUTPUT_DIR = Path("ml/data/final_data")
N_AUGMENTATIONS = 1  # how many extra images per original

# Define augmentation pipeline
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"),
    tf.keras.layers.RandomRotation(0.4),
    tf.keras.layers.RandomZoom(0.3),
    tf.keras.layers.RandomContrast(0.2),
    tf.keras.layers.RandomTranslation(0.2, 0.2),
])

# Create output directories
for split in ['train', 'val']:
    for class_dir in (INPUT_DIR / split).iterdir():
        if class_dir.is_dir():
            (OUTPUT_DIR / split / class_dir.name).mkdir(parents=True, exist_ok=True)

# Function to augment and save
def augment_and_save(image_path, output_folder, base_name):
    img_raw = tf.io.read_file(str(image_path))
    img = tf.image.decode_image(img_raw, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)  # normalize 0-1

    # Save the original image too
    tf.keras.preprocessing.image.save_img(str(output_folder / f"{base_name}_orig.jpg"), img)

    # Save augmented images
    for i in range(N_AUGMENTATIONS):
        augmented = data_augmentation(tf.expand_dims(img, axis=0))
        augmented = tf.squeeze(augmented, axis=0)
        out_path = output_folder / f"{base_name}_aug_{i}.jpg"
        tf.keras.preprocessing.image.save_img(str(out_path), augmented)

# Walk through train/val/test splits
for split in ['train', 'val']:
    split_dir = INPUT_DIR / split
    for class_dir in tqdm(list(split_dir.iterdir()), desc=f"Processing {split} set"):
        if class_dir.is_dir():
            for img_file in class_dir.glob("*.*"):
                output_class_dir = OUTPUT_DIR / split / class_dir.name
                base_name = img_file.stem  # filename without extension
                augment_and_save(img_file, output_class_dir, base_name)

print("\n✅ Augmentation and saving complete!")
