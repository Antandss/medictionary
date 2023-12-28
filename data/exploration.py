import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database
db_path = 'medictionary/data/fictive_patients.db'
conn = sqlite3.connect(db_path)

# Read data into a pandas DataFrame
query = 'SELECT * FROM patients'
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Display basic information about the dataset
print("Basic Information about the Dataset:")
print(df.info())

# Display summary statistics for numerical columns
print("\nSummary Statistics:")
print(df.describe())

# Count of patients per condition
condition_counts = df['Condition'].value_counts()

# Plot a bar chart for the count of patients per condition
plt.figure(figsize=(12, 6))
sns.barplot(x=condition_counts.index, y=condition_counts.values, palette="viridis")
plt.title('Count of Patients per Condition')
plt.xlabel('Condition')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.show()

# Box plot of age distribution per condition
plt.figure(figsize=(12, 6))
sns.boxplot(x='Condition', y='Age', data=df, palette="muted")
plt.title('Age Distribution per Condition')
plt.xlabel('Condition')
plt.ylabel('Age')
plt.xticks(rotation=45, ha='right')
plt.show()

# Pair plot for numerical variables
sns.pairplot(df, hue='Condition', palette='Set2')
plt.suptitle('Pair Plot of Numerical Variables', y=1.02)
plt.show()