import sqlite3
import random

# Connect to the SQLite database (create it if it doesn't exist)
db_path = 'medictionary/data/fictive_patients.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the 'patients' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        Patient_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Age INTEGER,
        Gender TEXT,
        Condition TEXT,
        Medication TEXT
    )
''')

# Specify the number of patients
num_patients = 500

# Define possible medical conditions and associated medications
conditions_and_meds = {
    'Hypertension': ['Medication_H1', 'Medication_H2', 'Medication_H3'],
    'Diabetes': ['Medication_D1', 'Medication_D2', 'Medication_D3'],
    'Arthritis': ['Medication_A1', 'Medication_A2', 'Medication_A3'],
    'Migraine': ['Medication_M1', 'Medication_M2', 'Medication_M3']
}

# Generate synthetic data and insert into the database
for i in range(1, num_patients + 1):
    condition = random.choice(list(conditions_and_meds.keys()))

    medication = random.choice(conditions_and_meds[condition])

    cursor.execute('''
        INSERT INTO patients (Patient_ID, Name, Age, Gender, Condition, Medication)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        i,
        f'Patient_{i}',
        random.randint(18, 75),
        random.choice(['Male', 'Female']),
        condition,
        medication
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()