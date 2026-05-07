import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv("../mess_data.csv")

print("Dataset Loaded Successfully!\n")

print(df.head())

# -----------------------------------
# ENCODE CATEGORICAL FEATURES
# -----------------------------------

label_encoders = {}

categorical_columns = [
    "day_of_week",
    "weather"
]

for column in categorical_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(df[column])

    label_encoders[column] = encoder

# -----------------------------------
# INPUT FEATURES (X)
# -----------------------------------

X = df[
    [
        "students_present",
        "day_of_week",
        "weather",
        "exam_week",
        "holiday",
        "menu_popularity",
        "temperature",
        "special_event"
    ]
]

# -----------------------------------
# TARGET VARIABLE (y)
# -----------------------------------

y = df["rice_consumed_kg"]

# -----------------------------------
# TRAIN TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nData Split Completed!")
print(f"Training Rows: {len(X_train)}")
print(f"Testing Rows: {len(X_test)}")

# -----------------------------------
# TRAIN MODEL
# -----------------------------------

model = LinearRegression()

model.fit(X_train, y_train)

print("\nModel Trained Successfully!")

# -----------------------------------
# MAKE PREDICTIONS
# -----------------------------------

y_pred = model.predict(X_test)

# -----------------------------------
# EVALUATE MODEL
# -----------------------------------

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(y_test, y_pred)

print("\nMODEL EVALUATION")
print("-" * 30)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R2 Score : {r2:.4f}")

# -----------------------------------
# SAVE MODEL
# -----------------------------------

joblib.dump(model, "food_waste_model.pkl")

print("\nModel Saved Successfully!")

# -----------------------------------
# SAVE LABEL ENCODERS
# -----------------------------------

joblib.dump(label_encoders, "label_encoders.pkl")

print("Label Encoders Saved Successfully!")