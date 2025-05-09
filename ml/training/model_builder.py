import tensorflow as tf

# Settings
IMG_HEIGHT = 224
IMG_WIDTH = 224
NUM_CLASSES = 8

def build_model():

    # Data Augmentation block
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.4),
        tf.keras.layers.RandomZoom(0.3),
        tf.keras.layers.RandomBrightness(0.2),
    ], name="data_augmentation")

    # Load EfficientNetB0 without top layers
    base_model = tf.keras.applications.EfficientNetB2(
        include_top=False,
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
        weights="imagenet",
        pooling=None
    )
    base_model.trainable = False  # Freeze it
    
    # Build the full model
    inputs = tf.keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3), name="input_layer")
    x = data_augmentation(inputs)
    x = tf.keras.applications.efficientnet.preprocess_input(x)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    x = tf.keras.layers.Dense(512, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    x = tf.keras.layers.Dense(256, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs, name="EfficientNetB0_Leaf_Classifier")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    model = build_model()
    model.summary()
