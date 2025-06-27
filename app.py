# app.py (Flask Backend)
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load("fraud_model.pkl")
scaler = joblib.load("scaler.pkl")  # Save your scaler when training

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Define the expected input fields from the form
        input_fields = [
            'transaction_amount',
            'account_balance_before',
            'account_balance_after',
            'receiver_balance_before',
            'receiver_balance_after',
            'hour_of_day'
        ]

        # Extract and convert input values from the form
        features = [float(request.form[field]) for field in input_fields]
        input_data = np.array(features).reshape(1, -1)

        # Scale the input features
        input_scaled = scaler.transform(input_data)

        # Predict using the trained model
        prediction = model.predict(input_scaled)[0]
        result = "🚨 Fraudulent Transaction Detected!" if prediction == 1 else "✅ Transaction is Legitimate."

        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
