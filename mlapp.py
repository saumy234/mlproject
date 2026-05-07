from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import pandas as pd
import joblib
import sqlite3

from datetime import datetime

# ---------------------------------------
# INITIALIZE FLASK APP
# ---------------------------------------

app = Flask(__name__)

CORS(app)

# ---------------------------------------
# LOAD TRAINED MODEL
# ---------------------------------------

model = joblib.load(
    "model/food_waste_model.pkl"
)

label_encoders = joblib.load(
    "model/label_encoders.pkl"
)

print("Model Loaded Successfully!")

# ---------------------------------------
# DATABASE CONNECTION
# ---------------------------------------

def connect_db():

    conn = sqlite3.connect(
        "food_waste.db"
    )

    conn.row_factory = sqlite3.Row

    return conn

# ---------------------------------------
# CREATE DATABASE TABLE
# ---------------------------------------

conn = connect_db()

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    time TEXT,

    students INTEGER,

    prediction REAL,

    waste REAL,

    efficiency REAL,

    risk TEXT,

    savings REAL,

    manual REAL,

    ai_insight TEXT
)

""")

conn.commit()

conn.close()

# ---------------------------------------
# HOME ROUTE
# ---------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# ---------------------------------------
# HISTORY ROUTE
# ---------------------------------------

@app.route("/history")
def history():

    try:

        conn = connect_db()

        cursor = conn.cursor()

        history_data = cursor.execute("""

        SELECT * FROM predictions

        ORDER BY id DESC

        LIMIT 10

        """).fetchall()

        conn.close()

        prediction_history = []

        for row in history_data:

            prediction_history.append({

                "time": row["time"],

                "students": row["students"],

                "prediction": row["prediction"],

                "waste": row["waste"]
            })

        return jsonify({

            "history": prediction_history
        })

    except Exception as e:

        return jsonify({

            "error": str(e)
        })

# ---------------------------------------
# LATEST PREDICTION ROUTE
# ---------------------------------------

@app.route("/latest")
def latest_prediction():

    try:

        conn = connect_db()

        cursor = conn.cursor()

        latest = cursor.execute("""

        SELECT * FROM predictions

        ORDER BY id DESC

        LIMIT 1

        """).fetchone()

        conn.close()

        if latest is None:

            return jsonify({

                "message": "No prediction found"
            })

        return jsonify({

            "prediction":
            latest["prediction"],

            "waste":
            latest["waste"],

            "efficiency":
            latest["efficiency"],

            "risk":
            latest["risk"],

            "savings":
            latest["savings"],

            "manual":
            latest["manual"],

            "ai_insight":
            latest["ai_insight"]
        })

    except Exception as e:

        return jsonify({

            "error": str(e)
        })

# ---------------------------------------
# PREDICTION ROUTE
# ---------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        students_present = int(
            data["students_present"]
        )

        day_of_week = data[
            "day_of_week"
        ]

        weather = data[
            "weather"
        ]

        exam_week = int(
            data["exam_week"]
        )

        holiday = int(
            data["holiday"]
        )

        menu_popularity = int(
            data["menu_popularity"]
        )

        temperature = int(
            data["temperature"]
        )

        special_event = int(
            data["special_event"]
        )

        # -----------------------------------
        # ENCODE FEATURES
        # -----------------------------------

        day_encoded = label_encoders[
            "day_of_week"
        ].transform([day_of_week])[0]

        weather_encoded = label_encoders[
            "weather"
        ].transform([weather])[0]

        # -----------------------------------
        # CREATE INPUT DATAFRAME
        # -----------------------------------

        input_data = pd.DataFrame([[
            students_present,
            day_encoded,
            weather_encoded,
            exam_week,
            holiday,
            menu_popularity,
            temperature,
            special_event
        ]], columns=[

            "students_present",
            "day_of_week",
            "weather",
            "exam_week",
            "holiday",
            "menu_popularity",
            "temperature",
            "special_event"
        ])

        # -----------------------------------
        # MODEL PREDICTION
        # -----------------------------------

        prediction = model.predict(
            input_data
        )[0]

        prediction = round(
            prediction,
            2
        )

        # -----------------------------------
        # CALCULATIONS
        # -----------------------------------

        recommended_preparation = round(
            prediction * 1.05,
            2
        )

        estimated_waste = round(
            recommended_preparation - prediction,
            2
        )

        waste_risk = "Low"

        if estimated_waste > 10:

            waste_risk = "High"

        elif estimated_waste > 6:

            waste_risk = "Medium"

        efficiency_score = round(

            (1 - (
                estimated_waste /
                recommended_preparation
            )) * 100,

            2
        )

        monthly_savings = round(

            estimated_waste * 30,

            2
        )

        manual_estimate = round(

            students_present * 0.14,

            2
        )

        # -----------------------------------
        # AI INSIGHTS
        # -----------------------------------

        ai_insights = []

        if weather == "Rainy" and exam_week == 1:

            ai_insights.append(
                "Rain and exams may reduce attendance."
            )

        if menu_popularity >= 8:

            ai_insights.append(
                "Highly popular menu detected."
            )

        if holiday == 1:

            ai_insights.append(
                "Holiday may reduce occupancy."
            )

        if special_event == 1:

            ai_insights.append(
                "Special events can increase attendance."
            )

        if students_present > 900:

            ai_insights.append(
                "Very high hostel occupancy detected."
            )

        if waste_risk == "High":

            ai_insights.append(
                "High waste risk detected."
            )

        final_ai_insight = " ".join(
            ai_insights
        )

        # -----------------------------------
        # SAVE INTO DATABASE
        # -----------------------------------

        conn = connect_db()

        cursor = conn.cursor()

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        cursor.execute("""

        INSERT INTO predictions (

            time,
            students,
            prediction,
            waste,
            efficiency,
            risk,
            savings,
            manual,
            ai_insight

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            current_time,
            students_present,
            prediction,
            estimated_waste,
            efficiency_score,
            waste_risk,
            monthly_savings,
            manual_estimate,
            final_ai_insight
        ))

        conn.commit()

        # -----------------------------------
        # FETCH HISTORY
        # -----------------------------------

        history_data = cursor.execute("""

        SELECT * FROM predictions

        ORDER BY id DESC

        LIMIT 10

        """).fetchall()

        conn.close()

        prediction_history = []

        for row in history_data:

            prediction_history.append({

                "time": row["time"],

                "students": row["students"],

                "prediction": row["prediction"],

                "waste": row["waste"]
            })

        # -----------------------------------
        # RETURN RESPONSE
        # -----------------------------------

        return jsonify({

            "predicted_rice_consumption_kg":
            prediction,

            "recommended_preparation_kg":
            recommended_preparation,

            "estimated_waste_kg":
            estimated_waste,

            "waste_risk":
            waste_risk,

            "efficiency_score":
            efficiency_score,

            "monthly_savings":
            monthly_savings,

            "manual_estimate":
            manual_estimate,

            "ai_insight":
            final_ai_insight,

            "history":
            prediction_history
        })

    except Exception as e:

        return jsonify({

            "error": str(e)
        })

# ---------------------------------------
# RUN SERVER
# ---------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )