def connect_to_database(name='database.db'):
    import sqlite3
    return sqlite3.connect(name, check_same_thread=False)

def init_db(connection):
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0.0
    )
''')
    connection.commit()

def add_user(connection, username, password, email):
    cursor = connection.cursor()
    query = '''INSERT INTO users (username, password, email) VALUES (?, ?, ?)'''
    cursor.execute(query,(username, password, email))
    connection.commit()

def get_user(connection, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE username = ?'''
    cursor.execute(query,(username,))
    return cursor.fetchone()