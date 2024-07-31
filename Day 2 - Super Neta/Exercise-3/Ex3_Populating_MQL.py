import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Load the Excel file into a pandas DataFrame
file_path = r'C:\Users\prerk\OneDrive\Desktop\Prerana\PESU\LLM Special Topic\Day 2 - Super Neta\Exercise-3\Assembly_Segments.xlsx'
df = pd.read_excel(file_path)
df = df.dropna()

# Database connection details
db_config = {
    'user': 'root',
    'password': 'MySQLPass123$',
    'host': 'localhost',
    'database': 'assembly_segments'
}

# Define table creation query
table_name = 'election_data'
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    State_UT_Code_Name VARCHAR(255),
    PC_NO INT,
    PC_NAME VARCHAR(255),
    AC_NO INT,
    AC_NAME VARCHAR(255),
    TOTAL_ELECTORS INT,
    TOTAL_VOTES_IN_STATE INT,
    NOTA_VOTES_EVM INT,
    CANDIDATE_NAME VARCHAR(255),
    PARTY VARCHAR(255),
    VOTES_SECURED_EVM INT
);
"""

# Connect to MySQL and execute the query
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()

    # Insert data into the table
    for _, row in df.iterrows():
        insert_query = f"""
        INSERT INTO {table_name} (
            State_UT_Code_Name, PC_NO, PC_NAME, AC_NO, AC_NAME,
            TOTAL_ELECTORS, TOTAL_VOTES_IN_STATE, NOTA_VOTES_EVM,
            CANDIDATE_NAME, PARTY, VOTES_SECURED_EVM
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, tuple(row))
    
    conn.commit()
    print("Data inserted successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)
finally:
    cursor.close()
    conn.close()
