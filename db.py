import sqlite3

DATABASE = 'pimeet.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS trainers (
    id TEXT PRIMARY KEY,
    trainer_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    mobile TEXT NOT NULL UNIQUE,
    status TEXT CHECK(status IN ('Active', 'Inactive')) NOT NULL,
    bio TEXT,
    profile_image BLOB
)
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            description TEXT NOT NULL,
            trainer_id TEXT,
            meet_id TEXT UNIQUE,
            FOREIGN KEY (trainer_id) REFERENCES trainers(id)
        )
    ''')

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        contact TEXT,
        profile_pic BLOB,
        profile_pic_type TEXT
    )
''')



    conn.commit()
    conn.close()
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
