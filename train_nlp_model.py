import os
import pandas as pd
import joblib
import numpy as np

from sentence_transformers import SentenceTransformer

from sklearn.model_selection import train_test_split

from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from modules.agriculture_nlp import clean_text


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "data/agriculture_symptoms.csv"

MODEL_DIR = "models"

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# START
# ============================================================

print("=" * 70)

print("AGRIMIND AI - AGRICULTURE SYMPTOM NLP TRAINING")

print("=" * 70)


# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(
    DATASET_PATH
)

print(
    "Original Dataset Shape:",
    df.shape
)

print(
    "Columns:",
    df.columns.tolist()
)


# ============================================================
# VALIDATE DATA
# ============================================================

required_columns = [
    "label",
    "text"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(

            f"Missing required column: {column}"

        )


# ============================================================
# CLEAN DATASET
# ============================================================

print("\nCleaning dataset...")

df = df.dropna(
    subset=["label", "text"]
).copy()


df["label"] = (

    df["label"]
    .astype(str)
    .str.strip()

)


df["text"] = (

    df["text"]
    .astype(str)
    .apply(clean_text)

)


# Remove short text

df = df[
    df["text"].str.len() >= 5
].copy()


# Remove duplicates

df = df.drop_duplicates(
    subset=["label", "text"]
)


df = df.reset_index(
    drop=True
)


print(
    "Clean Dataset Shape:",
    df.shape
)


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

print("\nDisease Distribution:")

print(
    df["label"].value_counts()
)


print(
    "\nNumber of Diseases:",
    df["label"].nunique()
)


# ============================================================
# CREATE MODEL TEXT
# ============================================================

df["model_text"] = (

    "crop plant symptoms: "

    + df["text"]

)


# ============================================================
# TRAIN TEST SPLIT
# ============================================================

X = df["model_text"]

y = df["label"]


X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


print(
    "\nTraining Samples:",
    len(X_train)
)

print(
    "Testing Samples:",
    len(X_test)
)


# ============================================================
# LOAD SENTENCE TRANSFORMER
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"


print(
    "\nLoading Sentence Transformer..."
)


embedding_model = SentenceTransformer(
    MODEL_NAME
)


print(
    "Sentence Transformer Loaded Successfully"
)


# ============================================================
# CREATE TRAINING EMBEDDINGS
# ============================================================

print(
    "\nCreating Training Embeddings..."
)


X_train_embeddings = embedding_model.encode(

    X_train.tolist(),

    batch_size=32,

    show_progress_bar=True,

    convert_to_numpy=True,

    normalize_embeddings=True

)


print(
    "Training Embedding Shape:",
    X_train_embeddings.shape
)


# ============================================================
# CREATE TEST EMBEDDINGS
# ============================================================

print(
    "\nCreating Testing Embeddings..."
)


X_test_embeddings = embedding_model.encode(

    X_test.tolist(),

    batch_size=32,

    show_progress_bar=True,

    convert_to_numpy=True,

    normalize_embeddings=True

)


print(
    "Testing Embedding Shape:",
    X_test_embeddings.shape
)


# ============================================================
# TRAIN CLASSIFIER
# ============================================================

print(
    "\nTraining SVM Classifier..."
)


classifier = SVC(

    kernel="rbf",

    C=15,

    gamma="scale",

    probability=True,

    class_weight="balanced",

    random_state=42

)


classifier.fit(

    X_train_embeddings,

    y_train

)


print(
    "Classifier Training Completed"
)


# ============================================================
# TEST MODEL
# ============================================================

print(
    "\nTesting Model..."
)


y_pred = classifier.predict(
    X_test_embeddings
)


accuracy = accuracy_score(

    y_test,

    y_pred

)


print("\n" + "=" * 70)

print("MODEL PERFORMANCE")

print("=" * 70)


print(

    f"\nAccuracy: {accuracy * 100:.2f}%"

)


print(
    "\nClassification Report:\n"
)


print(

    classification_report(

        y_test,

        y_pred,

        zero_division=0

    )

)


# ============================================================
# CONFIDENCE ANALYSIS
# ============================================================

probabilities = classifier.predict_proba(
    X_test_embeddings
)


maximum_probabilities = np.max(

    probabilities,

    axis=1

)


print("\n" + "=" * 70)

print("CONFIDENCE ANALYSIS")

print("=" * 70)


print(

    f"Average Confidence: "

    f"{np.mean(maximum_probabilities) * 100:.2f}%"

)


print(

    f"Minimum Confidence: "

    f"{np.min(maximum_probabilities) * 100:.2f}%"

)


print(

    f"Maximum Confidence: "

    f"{np.max(maximum_probabilities) * 100:.2f}%"

)


# ============================================================
# SAVE MODELS
# ============================================================

print(
    "\nSaving Models..."
)


CLASSIFIER_PATH = os.path.join(

    MODEL_DIR,

    "agriculture_classifier.pkl"

)


EMBEDDING_PATH = os.path.join(

    MODEL_DIR,

    "agriculture_embedding_model.pkl"

)


CLASSES_PATH = os.path.join(

    MODEL_DIR,

    "agriculture_disease_classes.pkl"

)


joblib.dump(

    classifier,

    CLASSIFIER_PATH

)


joblib.dump(

    MODEL_NAME,

    EMBEDDING_PATH

)


joblib.dump(

    classifier.classes_,

    CLASSES_PATH

)


print("\n" + "=" * 70)

print("TRAINING COMPLETED SUCCESSFULLY")

print("=" * 70)


print("\nGenerated Files:")

print(
    CLASSIFIER_PATH
)

print(
    EMBEDDING_PATH
)

print(
    CLASSES_PATH
)