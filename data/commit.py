import sqlite3

# Connect
db_path = 'medictionary/data/fictive_patients.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
               
cursor.execute('''              
CREATE TABLE IF NOT EXISTS medical_history (
    history_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    patient_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
)
''')
  
# Commit the changes and close the connection
conn.commit()
conn.close()