import tensorflow as tf
from pathlib import Path
import pickle

from ml.preprocessing.data_loader import load_datasets
from model_builder import build_model

def main():
    # Settings
    EPOCHS = 20
    MODEL_DIR = Path("models")
    FINAL_MODEL_DIR = Path("ml/models")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    BEST_MODEL_PATH = FINAL_MODEL_DIR / "best_model_saved.keras"
    HISTORY_PATH = FINAL_MODEL_DIR / "history.pkl"

    # Load data
    train_ds, val_ds = load_datasets()

    # Build model
    model = build_model()

    # Callbacks
    checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
        filepath=str(BEST_MODEL_PATH),
        monitor="val_loss",
        save_best_only=True,
        save_weights_only=False,
        verbose=1
    )

    early_stopping_cb = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )

    # Train
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[checkpoint_cb, early_stopping_cb]
    )

    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save only training metrics (loss/accuracy), not Tensorflow objects
    training_history_dict = history.history
    with open(HISTORY_PATH, "wb") as f:
        pickle.dump(training_history_dict, f)

    print("✅ Training history saved at:", HISTORY_PATH)

    # model.save(FINAL_MODEL_DIR)  # Save final model to same path

    print("✅ Training complete. Best model saved at:", BEST_MODEL_PATH)

if __name__ == "__main__":
    main()
