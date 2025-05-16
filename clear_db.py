import sqlite3

def clear_database():
    conn = sqlite3.connect('pimeet.db')
    cursor = conn.cursor()

    try:
        # Start a transaction
        cursor.execute('BEGIN TRANSACTION')
        
        # Delete all meetings first (due to foreign key constraint)
        cursor.execute('DELETE FROM meetings')
        print('Deleted all meetings')
        
        # Then delete all trainers
        cursor.execute('DELETE FROM trainers')
        print('Deleted all trainers')
        
        # Commit the transaction
        conn.commit()
        print('Database cleared successfully')

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f'Error: {e}')

    finally:
        conn.close()

if __name__ == '__main__':
    clear_database()