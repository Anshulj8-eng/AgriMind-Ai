import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================================================
# 1. LOAD DATASET
# =========================================================

DATA_PATH = "data/crop_yield.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())


# =========================================================
# 2. DATE PROCESSING
# =========================================================

df["harvest_date"] = pd.to_datetime(
    df["harvest_date"],
    errors="coerce"
)

df["harvest_year"] = df["harvest_date"].dt.year
df["harvest_month"] = df["harvest_date"].dt.month

# Drop original date
df = df.drop(columns=["harvest_date"])


# =========================================================
# 3. REMOVE IDENTIFIER COLUMNS
# =========================================================

# These columns identify records/fields but don't represent
# useful agricultural characteristics.

df = df.drop(
    columns=["id", "field_id"],
    errors="ignore"
)


# =========================================================
# 4. DEFINE FEATURES AND TARGET
# =========================================================

TARGET = "yield_tpha"

X = df.drop(columns=[TARGET])

y = df[TARGET]


print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget:")
print(TARGET)


# =========================================================
# 5. IDENTIFY COLUMN TYPES
# =========================================================

categorical_features = [
    "crop_type",
    "region",
    "season"
]

numerical_features = [
    column
    for column in X.columns
    if column not in categorical_features
]


print("\nNumerical Features:")
print(numerical_features)

print("\nCategorical Features:")
print(categorical_features)


# =========================================================
# 6. TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================================================
# 7. PREPROCESSING
# =========================================================

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)


categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numerical_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)


# =========================================================
# 8. DEFINE MODELS
# =========================================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        ),

    "Gradient Boosting":
        GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            random_state=42
        )
}


# =========================================================
# 9. TRAIN AND EVALUATE
# =========================================================

results = {}

best_model = None
best_model_name = None
best_r2 = -np.inf


print("\n")
print("=" * 60)
print("MODEL TRAINING")
print("=" * 60)


for name, model in models.items():

    print(f"\nTraining: {name}")

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    pipeline.fit(
        X_train,
        y_train
    )

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    results[name] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R2   : {r2:.4f}")

    if r2 > best_r2:

        best_r2 = r2
        best_model = pipeline
        best_model_name = name


# =========================================================
# 10. DISPLAY RESULTS
# =========================================================

print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

for name, metrics in results.items():

    print(
        f"\n{name}"
        f"\n  MAE  : {metrics['MAE']:.4f}"
        f"\n  RMSE : {metrics['RMSE']:.4f}"
        f"\n  R2   : {metrics['R2']:.4f}"
    )


print("\n")
print("=" * 60)
print("BEST MODEL")
print("=" * 60)

print("Model:", best_model_name)
print("R2 Score:", round(best_r2, 4))


# =========================================================
# 11. SAVE MODEL
# =========================================================

MODEL_PATH = "models/yield_model.pkl"

joblib.dump(
    best_model,
    MODEL_PATH
)

print("\nModel saved successfully!")
print("Location:", MODEL_PATH)


# =========================================================
# 12. TEST ONE PREDICTION
# =========================================================

sample = X_test.iloc[[0]]

actual_value = y_test.iloc[0]

predicted_value = best_model.predict(sample)[0]

print("\n")
print("=" * 60)
print("SAMPLE PREDICTION")
print("=" * 60)

print(
    f"Actual Yield    : {actual_value:.2f} tons/hectare"
)

print(
    f"Predicted Yield : {predicted_value:.2f} tons/hectare"
)

print(
    f"Difference      : "
    f"{abs(actual_value - predicted_value):.2f}"
)

print("\nTraining completed successfully!")