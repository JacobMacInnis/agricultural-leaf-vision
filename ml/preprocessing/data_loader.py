import tensorflow as tf
from pathlib import Path

# Settings
BATCH_SIZE = 32
IMG_HEIGHT = 224
IMG_WIDTH = 224

def load_datasets():

    # Paths
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    PROCESSED_DIR = PROJECT_ROOT / "data" / "final_data"
    TRAIN_DIR = PROCESSED_DIR / "train"
    VAL_DIR = PROCESSED_DIR / "val"
    TEST_DIR = PROCESSED_DIR / "test"

    # Load datasets
    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR,
        seed=42,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        label_mode="categorical"  # One-hot encode labels
    )

    print(train_ds.class_names)
    assert len(train_ds.class_names) == 8, f"❌ Expected 13 classes but got {len(train_ds.class_names)} classes."

    val_ds = tf.keras.utils.image_dataset_from_directory(
        VAL_DIR,
        seed=42,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        label_mode="categorical"
    )

    # test_ds = tf.keras.utils.image_dataset_from_directory(
    #     TEST_DIR,
    #     seed=42,
    #     image_size=(IMG_HEIGHT, IMG_WIDTH),
    #     batch_size=BATCH_SIZE,
    #     label_mode="categorical"
    # )

    # Prefetch for faster performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
    # test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

    print("✅ Datasets loaded successfully.")

    return train_ds, val_ds