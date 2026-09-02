import os
import json
import io
import numpy as np
import tensorflow as tf
from PIL import Image


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "plant_disease_model.keras"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "disease_classes.json"
)

IMG_SIZE = (224, 224)


# =========================================================
# CHECK REQUIRED FILES
# =========================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Disease model not found at:\n{MODEL_PATH}"
    )

if not os.path.exists(CLASS_PATH):
    raise FileNotFoundError(
        f"Disease classes file not found at:\n{CLASS_PATH}"
    )


# =========================================================
# LOAD MODEL
# =========================================================

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)


# =========================================================
# LOAD CLASS NAMES
# =========================================================

with open(CLASS_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)


# =========================================================
# IMAGE PREPROCESSING
# =========================================================

def preprocess_image(uploaded_file):

    try:

        # -----------------------------------------
        # CASE 1: Streamlit UploadedFile
        # -----------------------------------------

        if hasattr(uploaded_file, "getvalue"):

            image_bytes = uploaded_file.getvalue()

            image = Image.open(
                io.BytesIO(image_bytes)
            )

        # -----------------------------------------
        # CASE 2: Bytes
        # -----------------------------------------

        elif isinstance(uploaded_file, bytes):

            image = Image.open(
                io.BytesIO(uploaded_file)
            )

        # -----------------------------------------
        # CASE 3: File path
        # -----------------------------------------

        elif isinstance(uploaded_file, str):

            image = Image.open(uploaded_file)

        # -----------------------------------------
        # CASE 4: File-like object
        # -----------------------------------------

        else:

            image = Image.open(uploaded_file)


        # Convert PIL Image to RGB
        image = image.convert("RGB")


        # Resize image
        image = image.resize(IMG_SIZE)


        # Convert to NumPy
        image_array = np.array(
            image,
            dtype=np.float32
        )


        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        return image_array


    except Exception as e:

        raise RuntimeError(
            f"Image preprocessing failed: {str(e)}"
        )


# =========================================================
# DISEASE PREDICTION
# =========================================================

def predict_disease(uploaded_file):

    try:

        print("\n===================================")
        print("DISEASE DETECTION STARTED")
        print("Input type:", type(uploaded_file))
        print("===================================")


        # -----------------------------------------
        # PREPROCESS IMAGE
        # -----------------------------------------

        image_array = preprocess_image(
            uploaded_file
        )


        # -----------------------------------------
        # IMPORTANT
        # MobileNetV2 preprocessing
        # -----------------------------------------

        image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
            image_array
        )


        # -----------------------------------------
        # MODEL PREDICTION
        # -----------------------------------------

        predictions = model.predict(
            image_array,
            verbose=0
        )


        # -----------------------------------------
        # GET PREDICTED CLASS
        # -----------------------------------------

        predicted_index = int(
            np.argmax(predictions[0])
        )


        confidence = float(
            predictions[0][predicted_index]
        )


        # Safety check
        if predicted_index >= len(class_names):

            raise ValueError(
                f"Predicted index {predicted_index} "
                f"is outside class range."
            )


        disease = class_names[
            predicted_index
        ]


        print("Predicted Disease:", disease)
        print("Confidence:", confidence)
        print("===================================\n")


        return {
            "disease": disease,
            "confidence": confidence
        }


    except Exception as e:

        print("\nDISEASE DETECTION ERROR")
        print(str(e))

        raise RuntimeError(
            f"Disease prediction failed: {str(e)}"
        )