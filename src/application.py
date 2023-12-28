from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='/Users/anthonandersson/software/medictionary/templates')

# Function to simulate a machine learning model
def recommend_medication(patient_id, condition):
    # Replace this with NN
    # For now using a simple mapping for debug
    condition_medication_mapping = {
        'Hypertension': 'Medication_H1',
        'Diabetes': 'Medication_D1',
        'Arthritis': 'Medication_A1',
        'Migraine': 'Medication_M1'
    }
    return condition_medication_mapping.get(condition, 'Unknown Medication')
# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from the form
        patient_id = request.form.get('patient_id')
        gender = request.form.get('gender')
        condition = request.form.get('condition')

        # Connect to the SQLite database
        conn = sqlite3.connect('/Users/anthonandersson/software/medictionary/data/fictive_patients.db') #Need to change absolute
        cursor = conn.cursor()

        # Query the database to get patient information
        query = f"SELECT * FROM patients WHERE Patient_ID = {patient_id}"
        cursor.execute(query)
        patient_data = cursor.fetchone()

        # Close the database connection
        conn.close()

        if patient_data:
            # Get medication recommendation from the machine learning model
            medication_recommendation = recommend_medication(patient_id, condition)

            return render_template('result.html', patient_data=patient_data, medication_recommendation=medication_recommendation)
        else:
            return render_template('error.html')

    return render_template('index.html')
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)