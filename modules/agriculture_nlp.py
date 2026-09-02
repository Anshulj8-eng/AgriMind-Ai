import os
import joblib
import numpy as np


# =========================================================
# PROJECT PATH CONFIGURATION
# =========================================================

# Current file:
# AgriMind/modules/agriculture_nlp.py

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up:
# AgriMind/
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

# Models folder:
# AgriMind/models/
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

# Model file
MODEL_PATH = os.path.join(
    MODELS_DIR,
    "agriculture_classifier.pkl"
)


# =========================================================
# LOAD MODEL
# =========================================================

model = None


def load_agriculture_model():
    global model

    try:

        print("\n" + "=" * 60)
        print("AGRICULTURE NLP MODEL DEBUG")
        print("=" * 60)

        print("Current module directory:")
        print(CURRENT_DIR)

        print("\nProject root:")
        print(PROJECT_ROOT)

        print("\nModels directory:")
        print(MODELS_DIR)

        print("\nExpected model path:")
        print(MODEL_PATH)

        print("\nModels directory exists:")
        print(os.path.exists(MODELS_DIR))

        print("\nModel file exists:")
        print(os.path.exists(MODEL_PATH))

        # Show all files inside models folder
        if os.path.exists(MODELS_DIR):

            print("\nFiles inside models folder:")

            for file in os.listdir(MODELS_DIR):
                print(" -", file)

        else:

            print("\nERROR: Models folder does not exist!")

            return None

        # Check model
        if not os.path.isfile(MODEL_PATH):

            print("\nERROR: agriculture_classifier.pkl NOT FOUND")

            return None

        # Load model
        print("\nLoading agriculture NLP model...")

        loaded_model = joblib.load(MODEL_PATH)

        print("SUCCESS: Agriculture NLP model loaded!")

        print("=" * 60 + "\n")

        return loaded_model

    except Exception as e:

        print("\nERROR LOADING AGRICULTURE NLP MODEL")
        print(type(e).__name__)
        print(str(e))

        return None


# Load model when module starts
model = load_agriculture_model()


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    if text is None:
        return ""

    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove extra spaces
    text = " ".join(text.split())

    return text


# =========================================================
# PREDICT SYMPTOM / DISEASE
# =========================================================

def predict_agriculture_symptom(text):

    global model

    if model is None:

        return {
            "success": False,
            "disease": "Model Not Loaded",
            "confidence": 0,
            "message": (
                "Agriculture NLP model could not be loaded. "
                f"Expected location: {MODEL_PATH}"
            )
        }

    try:

        # Clean user input
        cleaned_text = clean_text(text)

        if len(cleaned_text.strip()) == 0:

            return {
                "success": False,
                "disease": "No Input",
                "confidence": 0,
                "message": "Please enter crop symptoms."
            }

        # =================================================
        # PREDICTION
        # =================================================

        prediction = model.predict([cleaned_text])[0]

        confidence = 0.0

        # Check whether model supports probability
        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba([cleaned_text])[0]

            confidence = float(np.max(probabilities)) * 100

        return {

            "success": True,

            "disease": str(prediction),

            "confidence": round(confidence, 2),

            "message": (
                f"Based on the symptoms, the possible issue is {prediction}."
            )

        }

    except Exception as e:

        print("Prediction Error:", str(e))

        return {

            "success": False,

            "disease": "Prediction Error",

            "confidence": 0,

            "message": str(e)

        }


# =========================================================
# GET MODEL STATUS
# =========================================================

def get_model_status():

    return {

        "model_loaded": model is not None,

        "model_path": MODEL_PATH,

        "model_exists": os.path.exists(MODEL_PATH),

        "models_directory": MODELS_DIR

    }