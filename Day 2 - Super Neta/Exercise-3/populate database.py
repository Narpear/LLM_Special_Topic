import pandas as pd
import sqlite3

# Load the data from the Excel file
file_path = 'Assembly_Election.xlsx'  # Adjust the file path if necessary
df = pd.read_excel(file_path)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('election_results.db')

# Create a cursor object
cursor = conn.cursor()

# Create table with more descriptive field names
cursor.execute('''
CREATE TABLE IF NOT EXISTS election_results (
    state_name TEXT,
    parliamentary_constituency_no INTEGER,
    parliamentary_constituency_name TEXT,
    assembly_constituency_no INTEGER,
    assembly_constituency_name TEXT,
    total_electors INTEGER,
    total_votes_in_state INTEGER,
    nota_votes INTEGER,
    candidate_name TEXT,
    party TEXT,
    votes_secured INTEGER
)
''')

# Iterate through the DataFrame and insert each row into the database
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO election_results (
        state_name,
        parliamentary_constituency_no,
        parliamentary_constituency_name,
        assembly_constituency_no,
        assembly_constituency_name,
        total_electors,
        total_votes_in_state,
        nota_votes,
        candidate_name,
        party,
        votes_secured
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['State-UT Code & Name'],
        row['PC NO'],
        row['PC NAME'],
        row['AC NO'],
        row['AC NAME'],
        row['TOTAL ELECTORS'],
        row['TOTAL VOTES IN STATE'],
        row['NOTA VOTES EVM'],
        row['CANDIDATE NAME'],
        row['PARTY'],
        row['VOTES SECURED EVM']
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()
