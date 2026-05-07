# AI Hostel Food Waste Prediction System

An AI-powered Hostel Food Waste Prediction and Analytics System built using Machine Learning, Flask, SQLite, HTML, CSS, JavaScript, and Chart.js.

This project predicts hostel food consumption using Linear Regression and provides intelligent analytics to reduce food wastage in hostel mess operations.

---

# Project Objective

Food wastage is one of the major operational problems in hostel mess systems.

This project aims to:

- Predict daily food consumption
- Reduce unnecessary food preparation
- Analyze mess efficiency
- Track food waste trends
- Provide AI-generated operational insights
- Build a continuous learning food analytics system

---

# Features

## Machine Learning Prediction
- Predicts rice consumption using Linear Regression

## Smart Inputs
The system considers:

- Students present
- Day of week
- Weather condition
- Exam week
- Holiday
- Menu popularity
- Temperature
- Special events

## AI Analytics Dashboard
- Predicted food consumption
- Estimated food waste
- Efficiency score
- Monthly waste estimation
- Smart AI insights

## Dynamic Visualization
- Interactive charts using Chart.js
- Prediction history visualization

## SQLite Database Integration
- Persistent prediction storage
- Prediction history survives refresh/restart

## Continuous Learning System
- Actual vs predicted comparison
- Error tracking
- Accuracy calculation
- Model performance monitoring

## Waste Risk Detection
- Low risk
- Medium risk
- High risk

---

# Technologies Used

## Frontend
- HTML
- CSS
- JavaScript
- Chart.js

## Backend
- Flask
- Flask-CORS

## Machine Learning
- Scikit-learn
- Linear Regression
- Pandas
- NumPy

## Database
- SQLite

---

# System Architecture

```text
Frontend Dashboard
        ↓
Flask API Backend
        ↓
Machine Learning Model
        ↓
SQLite Database
        ↓
Analytics + Prediction Engine
