import sqlite3

# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("antibiotic_resistance.db")
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries for convenience
    return conn

# Function to create the necessary database tables
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create the patients table with updated columns to match the application requirements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gender TEXT,
        age INTEGER,
        admission_department TEXT,
        previous_visits INTEGER,
        hospitalization_duration TEXT,
        last_exposure TEXT,
        region TEXT,
        ciprofloxacin INTEGER,  -- New column to track Ciprofloxacin usage
        resistance_in_urine INTEGER,  -- New column to track resistance in urine culture
        previous_resistance_to_antibiotics INTEGER,  -- New column for previous resistance to antibiotics
        diabetes INTEGER,
        hypertension INTEGER,
        chronic_lung_disease INTEGER,
        cardiovascular_disease INTEGER,
        resistance_prediction INTEGER  -- The prediction result
    )
    """)
    conn.commit()
    conn.close()

# Function to drop existing tables to reset schemma
def drop_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS patients")  
    conn.commit()
    conn.close()
    print("Dropped the patients table.")

# Uncomment drop table function to reset the db
# if __name__ == "__main__":
#     drop_tables()
#     create_tables()
