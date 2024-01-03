from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3

app = Flask(__name__, template_folder='/Users/anthonandersson/software/medictionary/templates')

# Function to simulate a machine learning model
def recommend_medication(patient_id, condition):
    # Replace this with NN
    # For now using a simple mapping
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        # Save the user to the database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


app.secret_key = 'your_secret_key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify credentials
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        # Retrieve user's medical history
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM medical_history WHERE user_id = ?', (user_id,))
        medical_history = cursor.fetchall()
        conn.close()

        return render_template('dashboard.html', medical_history=medical_history)

    return redirect(url_for('login'))

#app.secret_key = 'your_secret_key'

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)