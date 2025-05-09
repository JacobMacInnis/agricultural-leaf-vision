import tensorflow as tf

model = tf.keras.models.load_model("ml/models/best_model_saved.keras")
model.summary()
