import os
import json
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


# =========================================================
# CONFIGURATION
# =========================================================

DATA_DIR = "data/PlantVillage/PlantVillage"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "plant_disease_model.keras"
)

CLASS_PATH = os.path.join(
    MODEL_DIR,
    "disease_classes.json"
)

IMG_SIZE = (224, 224)

BATCH_SIZE = 16

EPOCHS = 10

VALIDATION_SPLIT = 0.20


# =========================================================
# CREATE MODEL DIRECTORY
# =========================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# =========================================================
# CHECK DATASET
# =========================================================

if not os.path.exists(DATA_DIR):

    raise FileNotFoundError(
        f"Dataset not found: {DATA_DIR}"
    )


print("=" * 60)
print("PLANT DISEASE DEEP LEARNING MODEL")
print("=" * 60)

print("\nDataset:")
print(DATA_DIR)


# =========================================================
# LOAD DATASET
# =========================================================

print("\nLoading images...")

train_dataset = tf.keras.utils.image_dataset_from_directory(

    DATA_DIR,

    validation_split=VALIDATION_SPLIT,

    subset="training",

    seed=42,

    image_size=IMG_SIZE,

    batch_size=BATCH_SIZE
)


validation_dataset = tf.keras.utils.image_dataset_from_directory(

    DATA_DIR,

    validation_split=VALIDATION_SPLIT,

    subset="validation",

    seed=42,

    image_size=IMG_SIZE,

    batch_size=BATCH_SIZE
)


# =========================================================
# CLASS NAMES
# =========================================================

class_names = train_dataset.class_names

num_classes = len(class_names)

print("\nNumber of classes:", num_classes)

print("\nClasses:")

for index, class_name in enumerate(class_names):

    print(
        index,
        "->",
        class_name
    )


# =========================================================
# SAVE CLASS NAMES
# =========================================================

with open(
    CLASS_PATH,
    "w"
) as file:

    json.dump(
        class_names,
        file,
        indent=4
    )


print(
    "\nClass names saved:",
    CLASS_PATH
)


# =========================================================
# PERFORMANCE OPTIMIZATION
# =========================================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    AUTOTUNE
)


# =========================================================
# DATA AUGMENTATION
# =========================================================

data_augmentation = models.Sequential([

    layers.RandomFlip(
        "horizontal"
    ),

    layers.RandomRotation(
        0.1
    ),

    layers.RandomZoom(
        0.1
    ),

])


# =========================================================
# MOBILE NET V2
# =========================================================

print("\nLoading MobileNetV2...")

base_model = MobileNetV2(

    input_shape=(
        IMG_SIZE[0],
        IMG_SIZE[1],
        3
    ),

    include_top=False,

    weights="imagenet"
)


# Freeze pretrained layers

base_model.trainable = False


# =========================================================
# BUILD MODEL
# =========================================================

inputs = layers.Input(
    shape=(
        IMG_SIZE[0],
        IMG_SIZE[1],
        3
    )
)


x = data_augmentation(inputs)


x = tf.keras.applications.mobilenet_v2.preprocess_input(
    x
)


x = base_model(
    x,
    training=False
)


x = layers.GlobalAveragePooling2D()(x)


x = layers.Dropout(
    0.3
)(x)


outputs = layers.Dense(
    num_classes,
    activation="softmax"
)(x)


model = models.Model(
    inputs,
    outputs
)


# =========================================================
# COMPILE MODEL
# =========================================================

model.compile(

    optimizer="adam",

    loss="sparse_categorical_crossentropy",

    metrics=[
        "accuracy"
    ]
)


# =========================================================
# MODEL SUMMARY
# =========================================================

print("\nModel architecture:")

model.summary()


# =========================================================
# CALLBACKS
# =========================================================

early_stopping = EarlyStopping(

    monitor="val_accuracy",

    patience=3,

    restore_best_weights=True
)


checkpoint = ModelCheckpoint(

    MODEL_PATH,

    monitor="val_accuracy",

    save_best_only=True,

    verbose=1
)


# =========================================================
# TRAIN
# =========================================================

print("\n")
print("=" * 60)
print("STARTING TRAINING")
print("=" * 60)

history = model.fit(

    train_dataset,

    validation_data=validation_dataset,

    epochs=EPOCHS,

    callbacks=[
        early_stopping,
        checkpoint
    ]
)


# =========================================================
# FINAL EVALUATION
# =========================================================

print("\n")
print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

loss, accuracy = model.evaluate(
    validation_dataset
)

print(
    f"\nValidation Loss: {loss:.4f}"
)

print(
    f"Validation Accuracy: {accuracy * 100:.2f}%"
)


# =========================================================
# SAVE FINAL MODEL
# =========================================================

model.save(
    MODEL_PATH
)


print("\n")
print("=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)

print(
    "Model saved to:",
    MODEL_PATH
)

print(
    "Classes saved to:",
    CLASS_PATH
)