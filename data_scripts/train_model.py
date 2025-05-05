import tensorflow as tf
from pathlib import Path
import pickle


# Import your data loader and model builder
from data_loader import train_ds, val_ds
from model_builder import build_model

# Settings
EPOCHS = 1
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
BEST_MODEL_PATH = MODEL_DIR / "best_model.h5"
HISTORY_PATH = MODEL_DIR / "history.pkl"
SAVED_MODEL_DIR = MODEL_DIR / "best_model_saved.keras"

# Build the model
model = build_model()

# Take a small subset of training and validation data
small_train_ds = train_ds.take(100)  # 100 batches (~3200 images)
small_val_ds = val_ds.take(20)       # 20 batches (~640 images)

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

# Train the model
history = model.fit(
    # train_ds,
    small_train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=[checkpoint_cb, early_stopping_cb]
)

# Save training history
with open(HISTORY_PATH, "wb") as f:
    pickle.dump(history.history, f)

print("✅ Training history saved at:", HISTORY_PATH)

model.save(SAVED_MODEL_DIR)


print("✅ Training complete. Best model and history saved at:", BEST_MODEL_PATH)

