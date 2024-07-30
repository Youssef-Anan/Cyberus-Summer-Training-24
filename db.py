import utils
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
        balance REAL NOT NULL DEFAULT 0.0,
        pfp_url TEXT
    )
''')
    connection.commit()

def add_user(connection, username, password, email):
    cursor = connection.cursor()
    hashed_password = utils.hash_password(password)
    query = '''INSERT INTO users (username, password, email) VALUES (?, ?, ?)'''
    cursor.execute(query,(username, hashed_password, email))
    connection.commit()

def get_user(connection, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE username = ?'''
    cursor.execute(query,(username,))
    return cursor.fetchone()

def edit_user(connection, username, Nuser, Nemail,pfp_url):
    cursor = connection.cursor()
    query = '''UPDATE users SET username = ?, email = ?, pfp_url = ? WHERE username = ?'''
    cursor.execute(query, (Nuser, Nemail, pfp_url, username))
    connection.commit()
    print("User data updated successfully")

def seed_admin_user(connection):
    admin_username = 'admin'
    admin_password = 'Admin@2003'

    admin_user = get_user(connection, admin_username)
    if not admin_user:
        add_user(connection, admin_username, admin_password)
        print("Admin user seeded successfully.")

#---------------------------------------------------------------------------------------
def init_game_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT
            )
    ''')
    connection.commit()

def add_game(connection, title, description, price, image_url=None):
    cursor = connection.cursor()
    query = ''' INSERT INTO games (title, description, price, image_url) VALUES (?, ?, ?, ?)'''
    cursor.execute(query, (title, description, price, image_url))
    connection.commit()

