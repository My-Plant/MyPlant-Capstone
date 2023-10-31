# %%
# Import OS module
import os

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import callbacks, layers, Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# %%
import splitfolders
input_folder = "Sample"
splitfolders.ratio(input_folder, output="dataset", seed=100, ratio=(0.6, 0.2, 0.2), group_prefix=None)

# %%
# Configure variables for Transfer learning
image_size = 224
target_size = (image_size, image_size)
input_shape = (image_size, image_size, 3)
grid_shape = (1, image_size, image_size, 3)

batch_size = 32

# %%
dataset_root = r"C:\Users\DELL\Downloads\MyPlant\dataset"

train_dir = os.path.join(dataset_root, "train")
test_dir = os.path.join(dataset_root, "val")

# %%
# Define augmentations for train dataset and read the images
train_aug = ImageDataGenerator(
    # Rescale
    rescale=1/255.0,
    fill_mode="nearest",
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    shear_range=0.2,
)

# Read data from directory
train_data = train_aug.flow_from_directory(
    train_dir,
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode="categorical"
)

# %%
# Get the list of categories in training data
cats = list(train_data.class_indices.keys())

print(cats)

# %%
# Augmentations for test data
test_aug = ImageDataGenerator(
    rescale=1/255.0
)

# Read data from directory
test_data = test_aug.flow_from_directory(
    test_dir,
    target_size=(image_size, image_size),
    batch_size=batch_size,
    class_mode="categorical"
)

# %%
# Load the base model
mbnet_v2 = keras.applications.MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=input_shape
)

# Stop from being trainable
mbnet_v2.trainable = False

# %%
# Define the layers
inputs = keras.Input(shape=input_shape)
x = mbnet_v2(inputs, training = False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.2)(x)
x = tf.keras.layers.Dense(len(cats), activation="softmax")(x)

# Combine the model
model = Model(inputs=inputs, outputs=x)

# Summary
model.summary()

# %%
# Compile
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
early_stopping_cb = callbacks.EarlyStopping(monitor="loss", patience=3)

# %%
# Num epochs
epochs = 5

# Train model
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=epochs,
    batch_size=batch_size,
    validation_batch_size=batch_size,
    callbacks=[early_stopping_cb]
)

# %%
model.evaluate(test_data)

# %%
model.save("Model_1.h5")

# %%
from keras.models import load_model
import cv2
import numpy as np

model = load_model('Model_1.h5')
classes=list(train_data.class_indices.keys())
img = cv2.imread('SCAB.jpeg')
img = cv2.resize(img,(224,224))
img = np.reshape(img,[1,224,224,3])
img = img/255.0

predict = model.predict(img)
result = np.argmax(predict,axis=1)
print(classes[result[0]])

# %%
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# %%
import pathlib
tflite_model_file = pathlib.Path('./Model/Model_1.tflite')
tflite_model_file.write_bytes(tflite_model)

# %%
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()

plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
