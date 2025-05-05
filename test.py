import sqlite3

def print_students_table_schema():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('pimeet.db')
        cursor = conn.cursor()

        # Fetch schema of the students table
        cursor.execute("PRAGMA table_info(students)")
        schema_info = cursor.fetchall()

        # Print header
        print("Column ID | Column Name       | Data Type     | Not Null | Default | Primary Key")
        print("--------------------------------------------------------------------------")

        # Loop through and print each column's schema
        for col in schema_info:
            col_id, name, dtype, notnull, default_val, pk = col
            print(f"{col_id:<9} | {name:<17} | {dtype:<13} | {notnull:<8} | {str(default_val):<7} | {pk}")

        # Close connection
        conn.close()

    except sqlite3.Error as e:
        print("Error reading schema from database:", e)

# Call the function
print_students_table_schema()
