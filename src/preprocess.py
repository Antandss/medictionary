import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

# Connect to the SQLite database
db_path = '/Users/anthonandersson/software/medictionary/data/fictive_patients.db'
conn = sqlite3.connect(db_path)

# Query the data from the 'patients' table
query = 'SELECT * FROM patients'
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Preprocess the data
le = LabelEncoder()

# Encode categorical variables
df['Gender'] = le.fit_transform(df['Gender'])
df['Condition'] = le.fit_transform(df['Condition'])

# Split features (X) and labels (y)
X = df[['Age', 'Gender', 'Condition']]
y = df['Medication']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize numerical features (optional, depending on the model)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the processed data to a file (e.g., CSV)
pd.DataFrame(X_train, columns=['Age', 'Gender', 'Condition']).to_csv('data/processed_data/X_train.csv', index=False)
pd.DataFrame(X_test, columns=['Age', 'Gender', 'Condition']).to_csv('data/processed_data/X_test.csv', index=False)
pd.DataFrame(y_train, columns=['Age', 'Gender', 'Condition']).to_csv('data/processed_data/y_train.csv', index=False)
pd.DataFrame(y_test, columns=['Age', 'Gender', 'Condition']).to_csv('data/processed_data/y_test.csv', index=False)
