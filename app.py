from flask import Flask, render_template, request
import joblib
import numpy as np
from database import get_db_connection, create_tables
# Analysis imports- email and csv file import
import csv
from flask import send_file
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Initialize the database
create_tables()

# Load the trained model
model = joblib.load("logistic_regression_model.pkl")
# Load the feature names to ensure alignment
feature_names = joblib.load("logistic_regression_features.pkl")

# home page
@app.route("/")
def home():
    return render_template("CDSS.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Debug: Log the form data
        print("Form Data Received:", request.form)

        # Extract raw input features from form
        raw_features = {
            "age": int(request.form.get("age", 0)),
            "previous_visits": int(request.form.get("previous-visits", 0)),
            "gender_male": 1 if request.form.get("gender") == "male" else 0,
            "admission_department_outpatient": 1 if request.form.get("admission-department") == "outpatient" else 0,
            "hospitalization_duration_less_5_days": 1 if request.form.get("hospitalization-duration") == "less-5-days" else 0,
            "last_antibiotic_exposure_less_30_days": 1 if request.form.get("last-exposure") == "less-30-days" else 0,
            "region_pakistan": 1 if request.form.get("region") == "pakistan" else 0,
            "region_saudi_arabia": 1 if request.form.get("region") == "saudi-arabia" else 0,
            "region_united_kingdom": 1 if request.form.get("region") == "united-kingdom" else 0,
            "region_united_states": 1 if request.form.get("region") == "united-states" else 0,
            "ciprofloxacin": 1 if request.form.get("ciprofloxacin") == "on" else 0,
            "resistance_in_urine": 1 if request.form.get("resistance-in-urine") == "on" else 0,
            "previous_resistance_to_antibiotics": 1 if request.form.get("previous-resistance-to-antibiotics") == "on" else 0,
            "diabetes": 1 if request.form.get("diabetes") == "on" else 0,
            "hypertension": 1 if request.form.get("hypertension") == "on" else 0,
            "chronic_lung_disease": 1 if request.form.get("chronic-lung-disease") == "on" else 0,
            "cardiovascular_disease": 1 if request.form.get("cardiovascular-disease") == "on" else 0
        }

        #  aligning by reordering and adding missing features
        features = [raw_features.get(col, 0) for col in feature_names]
        features = np.array([features])  # Reshape for model input

        # Debugging steps: Log features and shape
        print("Features for Prediction:", features)
        print("Shape of Features:", features.shape)

        # Predict resistance
        prediction = model.predict(features)[0]

        # Save data to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO patients (
            gender, age, admission_department, previous_visits, hospitalization_duration,
            last_exposure, region, ciprofloxacin, resistance_in_urine, previous_resistance_to_antibiotics,
            diabetes, hypertension, chronic_lung_disease, cardiovascular_disease, resistance_prediction
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form.get("gender"), int(request.form.get("age", 0)), request.form.get("admission-department"),
            int(request.form.get("previous-visits", 0)), request.form.get("hospitalization-duration"),
            request.form.get("last-exposure"), request.form.get("region"),
            1 if request.form.get("ciprofloxacin") == "on" else 0,
            1 if request.form.get("resistance-in-urine") == "on" else 0,
            1 if request.form.get("previous-resistance-to-antibiotics") == "on" else 0,
            1 if request.form.get("diabetes") == "on" else 0,
            1 if request.form.get("hypertension") == "on" else 0,
            1 if request.form.get("chronic-lung-disease") == "on" else 0,
            1 if request.form.get("cardiovascular-disease") == "on" else 0,
            prediction
        ))
        conn.commit()
        conn.close()

        # Return result
        result = "Resistant" if prediction == 1 else "Not Resistant"
        return render_template("result.html", result=result, data=request.form)

    except Exception as e:
        # Debug: Log the error
        print("Error occurred:", e)
        return f"An error occurred: {e}"
    
   # Analysis page
@app.route("/analysis")
def analysis():
    # Fetch history from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    history = cursor.fetchall()
    conn.close()
    return render_template("analysis.html", history=history)

@app.route("/download-history")
def download_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()

    # Save as CSV
    file_path = "patient_history.csv"
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([desc[0] for desc in cursor.description])  # Write headers
        writer.writerows(rows)  # Write data

    return send_file(file_path, as_attachment=True)

@app.route("/email-history")
def email_history():
    # Fetch data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()

    # Save as CSV
    file_path = "patient_history.csv"
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([desc[0] for desc in cursor.description])  # Write headers
        writer.writerows(rows)  # Write data

    # Send email
    sender = "your_email@example.com"
    receiver = "receiver_email@example.com"
    subject = "Patient History Data"
    body = "Please find attached the patient history data."
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # reding file

    with open(file_path, "r") as file:
        attachment = MIMEText(file.read(), "csv")
        attachment.add_header("Content-Disposition", "attachment", filename="patient_history.csv")
        msg.attach(attachment)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, "your_password")
        server.send_message(msg)

    return "Email sent successfully!"

if __name__ == "__main__":
    app.run(debug=True)
