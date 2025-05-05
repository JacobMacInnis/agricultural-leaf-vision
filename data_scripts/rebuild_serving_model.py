import tensorflow as tf
from tensorflow import keras
from pathlib import Path

# Load your trained model
MODEL_DIR = Path("models/best_model_saved.keras")
EXPORT_DIR = Path("models/vertex_ready_model")

# Load the original trained model
base_model = keras.models.load_model(MODEL_DIR)

# ✅ THIS IS NEW — Compile the model after loading
base_model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",  # or whatever you used
    metrics=["accuracy"]
)

IMG_SIZE = (224, 224)

@tf.function(input_signature=[tf.TensorSpec([None], dtype=tf.string, name="b64")])
def serve_fn(b64_images):
    decoded = tf.map_fn(
        lambda x: tf.io.decode_jpeg(tf.io.decode_base64(x), channels=3),
        b64_images,
        dtype=tf.uint8
    )

    resized = tf.image.resize(decoded, IMG_SIZE)
    normalized = resized / 255.0

    preds = base_model(normalized)
    return {"predictions": preds}

# Save it properly for Vertex AI
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
tf.saved_model.save(
    base_model,
    str(EXPORT_DIR),
    signatures={"serving_default": serve_fn}
)

print(f"✅ Vertex-ready model saved at {EXPORT_DIR}")
