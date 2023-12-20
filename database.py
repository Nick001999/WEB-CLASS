import sqlite3
import os

# Database connection functions

def get_db_connection():
    con = sqlite3.connect('twitter.db')
    return con

# Database creation functions

def create_db():
    if not os.path.exists('twitter.db'):
        con = get_db_connection()
        con.close()

def create_tables():
    # Create tables if they do not exist
    con = get_db_connection()
    cursor = con.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            birthdate TEXT,
            email TEXT
        )
    """)

    # Tweets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            users_id INTEGER,
            content TEXT,
            likes INTEGER,
            FOREIGN KEY(users_id) REFERENCES users(id)
        )
    """)

    # Likes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            users_id INTEGER,
            tweets_id INTEGER,
            PRIMARY KEY (users_id, tweets_id),
            FOREIGN KEY(users_id) REFERENCES users(id),
            FOREIGN KEY(tweets_id) REFERENCES tweets(id)
        )
    """)

    con.commit()
    con.close()

# Tweet retrieval functions

def get_all_tweets():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT * FROM tweets
        INNER JOIN users ON users.id = tweets.users_id
        ORDER BY tweets.id DESC
    """)
    result = cursor.fetchall()
    tweets = [row for row in result]
    return tweets

def get_user(username):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    return row

# User and tweet addition functions

def add_user(username, password, birthdate, email):
    con = get_db_connection()
    cursor = con.cursor()
    print(hash(password))
    cursor.execute("""
        INSERT INTO users(username, password, birthdate, email)
        VALUES (?, ?, ?, ?)
    """, (username, password, birthdate, email))
    con.commit()

def add_tweet(text, user_id):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO tweets(content, users_id, likes)
        VALUES (?, ?, ?)
    """, (text, user_id, 0))
    con.commit()

# Tweet retrieval functions by user ID

def get_user_by_id(user_id):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    return row

def get_tweets_by_user_id(user_id):
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT * FROM tweets
        WHERE users_id=? ORDER BY id DESC
    """, (user_id,))
    result = cursor.fetchall()
    tweets = [row for row in result]
    return tweets
