import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from ml.preprocessing.data_loader import load_datasets
import tensorflow as tf

def main():
    # === Paths ===
    OUTPUT_DIR = "client/public/plots"
    history_path = Path("ml/models/history.pkl")

    if not history_path.exists():
        print("❌ No training history found.")
        return

    # === Load History ===
    with open(history_path, "rb") as f:
        history = pickle.load(f)

    # === Print out metrics ===
    print("\n=== Training Metrics ===")
    for key in history.keys():
        print(f"{key}: {history[key]}")

    # === Plot Loss ===
    plt.figure(figsize=(8, 6))
    plt.plot(history["loss"], label="Training Loss")
    plt.plot(history["val_loss"], label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss Over Epochs")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'loss_curve.png'))
    plt.close()

    # === Plot Accuracy ===
    if "accuracy" in history and "val_accuracy" in history:
        plt.figure(figsize=(8, 6))
        plt.plot(history["accuracy"], label="Training Accuracy")
        plt.plot(history["val_accuracy"], label="Validation Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.title("Training and Validation Accuracy Over Epochs")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(OUTPUT_DIR, 'accuracy_curve.png'))
        plt.close()

    # === Confusion Matrix and Classification Report ===
    # Load model
    model = tf.keras.models.load_model("ml/models/best_model_saved.keras")

    # Load *raw* validation dataset (not prefetched)
    val_ds_raw = tf.keras.utils.image_dataset_from_directory(
        "ml/data/processed_balanced/test",
        seed=42,
        image_size=(224, 224),
        batch_size=32,
        label_mode="categorical"
    )
    class_names = val_ds_raw.class_names

    # For speed, use prefetching version for predictions
    _, test_ds, = load_datasets()


    # Get true labels
    y_true = []
    for _, labels in test_ds.unbatch():
        y_true.append(np.argmax(labels.numpy()))
    y_true = np.array(y_true)

    # Get model predictions
    y_pred_probs = model.predict(test_ds, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # --- Confusion Matrix ---
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(class_names))))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)

    fig, ax = plt.subplots(figsize=(10,8))
    disp.plot(ax=ax, cmap='Blues', colorbar=False)
    plt.title('Confusion Matrix')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'confusion_matrix.png'))
    plt.close()

    # --- Classification Report (text only) ---
    print("\n=== Classification Report ===")
    print(classification_report(y_true, y_pred, target_names=class_names))

if __name__ == "__main__":
    main()
