import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def train_model(dataset_path, model_path):
    # Load dataset
    df = pd.read_csv(dataset_path)

    # Remove missing values
    df = df.dropna(subset=["text", "disease"])

    X = df["text"]
    y = df["disease"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # NLP + ML pipeline
    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2)
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000
            )
        )
    ])

    # Train
    model.fit(X_train, y_train)

    # Test
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("=" * 50)
    print("AGRICULTURE DISEASE CLASSIFIER")
    print("=" * 50)

    print(f"Dataset size: {len(df)}")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    # Save model
    joblib.dump(model, model_path)

    print(f"\nModel saved to: {model_path}")

    return model