# models/unet.py

# Note: This is a simplified U-Net for demonstration.
# A real-world implementation might be more complex.

import tensorflow as tf
from tensorflow.keras import layers, Model

def build_unet(input_shape=(256, 256, 12), num_classes=2):
    """
    Builds a simplified U-Net model.

    Args:
        input_shape (tuple): Shape of the input image patches (height, width, channels).
        num_classes (int): Number of output classes (e.g., 2 for flood/non-flood).

    Returns:
        tensorflow.keras.Model: The compiled U-Net model.
    """
    inputs = layers.Input(shape=input_shape)

    # --- Encoder (Down-sampling path) ---
    c1 = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(inputs)
    c1 = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(c1)
    p1 = layers.MaxPooling2D((2, 2))(c1)

    c2 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(p1)
    c2 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(c2)
    p2 = layers.MaxPooling2D((2, 2))(c2)

    # --- Bottleneck ---
    b = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(p2)
    b = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(b)

    # --- Decoder (Up-sampling path) ---
    u1 = layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(b)
    u1 = layers.concatenate([u1, c2])
    c3 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(u1)
    c3 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(c3)

    u2 = layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c3)
    u2 = layers.concatenate([u2, c1])
    c4 = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(u2)
    c4 = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(c4)

    # --- Output Layer ---
    # Use 'softmax' for multi-class or 'sigmoid' for binary classification.
    # Since we have flood (1) and non-flood (0), we can treat it as binary.
    # But softmax is more general.
    outputs = layers.Conv2D(num_classes, (1, 1), activation='softmax')(c4)

    model = Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    print("U-Net model built successfully.")
    model.summary()
    
    return model