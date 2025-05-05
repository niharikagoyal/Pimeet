import sqlite3
from flask import Response
import base64

DATABASE = 'pimeet.db'  # Use the same DB for both functions

def save_profile_image(file, user_id):
    if not file:
        return False  # Explicitly return False if no file

    image_data = file.read()

    # Save image binary (BLOB) to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET profile_image = ? WHERE id = ?", (image_data, user_id))
    conn.commit()
    conn.close()

    return True  # ✅ Explicitly return True on success



def get_image(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT profile_image FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        # image_data = base64.b64encode(row[0]).decode('utf-8')
        # print(image_data)
        print(row[0])
        return row[0]
    else:
        return 'No Image', 404
