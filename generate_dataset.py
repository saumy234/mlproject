import pandas as pd
import random
import numpy as np

# -----------------------------
# CONFIGURATION
# -----------------------------

NUM_ROWS = 1500

DAYS = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

WEATHER_TYPES = ["Sunny", "Rainy", "Cold"]

# -----------------------------
# DATA STORAGE
# -----------------------------

data = []

# -----------------------------
# DATA GENERATION LOOP
# -----------------------------

for _ in range(NUM_ROWS):

    # -------------------------
    # GENERATE INPUT FEATURES
    # -------------------------

    students_present = random.randint(600, 950)

    day_of_week = random.choice(DAYS)

    weather = random.choices(
        WEATHER_TYPES,
        weights=[60, 25, 15],
        k=1
    )[0]

    exam_week = random.choices(
        [0, 1],
        weights=[80, 20],
        k=1
    )[0]

    holiday = random.choices(
        [0, 1],
        weights=[85, 15],
        k=1
    )[0]

    special_event = random.choices(
        [0, 1],
        weights=[92, 8],
        k=1
    )[0]

    menu_popularity = random.randint(1, 10)

    # -------------------------
    # TEMPERATURE GENERATION
    # -------------------------

    if weather == "Sunny":
        temperature = random.randint(28, 38)

    elif weather == "Rainy":
        temperature = random.randint(20, 30)

    else:
        temperature = random.randint(10, 20)

    # -------------------------
    # BASE RICE CONSUMPTION
    # -------------------------

    rice_consumed = students_present * 0.12

    # -------------------------
    # MENU EFFECT
    # -------------------------

    if menu_popularity >= 8:
        rice_consumed *= 1.10

    elif menu_popularity <= 3:
        rice_consumed *= 0.92

    # -------------------------
    # WEATHER EFFECT
    # -------------------------

    if weather == "Rainy":
        rice_consumed *= 0.95

    elif weather == "Cold":
        rice_consumed *= 1.04

    # -------------------------
    # EXAM EFFECT
    # -------------------------

    if exam_week == 1:
        rice_consumed *= 0.90

    # -------------------------
    # HOLIDAY EFFECT
    # -------------------------

    if holiday == 1:
        rice_consumed *= 0.85

    # -------------------------
    # SPECIAL EVENT EFFECT
    # -------------------------

    if special_event == 1:
        rice_consumed *= 1.10

    # -------------------------
    # WEEKEND EFFECT
    # -------------------------

    if day_of_week in ["Saturday", "Sunday"]:
        rice_consumed *= 0.95

    # -------------------------
    # TEMPERATURE EFFECT
    # -------------------------

    if temperature > 35:
        rice_consumed *= 0.96

    elif temperature < 15:
        rice_consumed *= 1.05

    # -------------------------
    # ADD RANDOM HUMAN NOISE
    # -------------------------

    noise = random.uniform(-5, 5)

    rice_consumed += noise

    # -------------------------
    # FINAL CLEANUP
    # -------------------------

    rice_consumed = round(rice_consumed, 2)

    # Prevent impossible values
    rice_consumed = max(rice_consumed, 40)

    # -------------------------
    # STORE RECORD
    # -------------------------

    data.append([
        students_present,
        day_of_week,
        weather,
        exam_week,
        holiday,
        menu_popularity,
        temperature,
        special_event,
        rice_consumed
    ])

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(data, columns=[
    "students_present",
    "day_of_week",
    "weather",
    "exam_week",
    "holiday",
    "menu_popularity",
    "temperature",
    "special_event",
    "rice_consumed_kg"
])

# -----------------------------
# SAVE CSV
# -----------------------------

df.to_csv("mess_data.csv", index=False)

print("Dataset generated successfully!")
print(df.head())