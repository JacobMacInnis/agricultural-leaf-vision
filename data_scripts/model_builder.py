import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0

# Settings
IMG_HEIGHT = 224
IMG_WIDTH = 224
NUM_CLASSES = 13

def build_model():
    # Load EfficientNetB0 without top layers (include_top=False)
    base_model = EfficientNetB0(
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
        include_top=False,
        weights="imagenet"
    )
    
    # Freeze the base model
    base_model.trainable = False

    # Create the full model
    inputs = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3))
    x = base_model(inputs, training=False)  # Important: set training=False
    x = layers.GlobalAveragePooling2D()(x)  # Reduces tensor size
    x = layers.Dropout(0.2)(x)  # Regularization
    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = models.Model(inputs, outputs)

    # Compile the model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    model = build_model()
    model.summary()
