import os
import csv
from pathlib import Path

def count_images_in_directory(directory_path):
    class_counts = {}

    for class_dir in sorted(os.listdir(directory_path)):
        class_path = os.path.join(directory_path, class_dir)

        if os.path.isdir(class_path):
            num_images = len([
                file for file in os.listdir(class_path)
                if file.lower().endswith((".png", ".jpg", ".jpeg"))
            ])
            class_counts[class_dir] = num_images

    return class_counts

def save_counts_to_csv(counts, output_file):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Class Name", "Image Count"])
        for class_name, count in counts.items():
            writer.writerow([class_name, count])

def main():
    # Update this if needed
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    RAW_DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"

    counts = count_images_in_directory(RAW_DATA_DIR)

    # Save to CSV
    output_csv = PROJECT_ROOT / "ml" / "validation" / "class_counts.csv"
    output_csv.parent.mkdir(parents=True, exist_ok=True)  # create directory if missing
    save_counts_to_csv(counts, output_csv)

    print(f"✅ Saved class counts to {output_csv}")

if __name__ == "__main__":
    main()
