import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",               # your MySQL username
        password="Yuva@123",   # your MySQL password
        database="AgroBot"
    )

def register_user(name, password):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO users (name, password) VALUES (%s, %s)"
    cursor.execute(query, (name, password))
    conn.commit()
    conn.close()

def validate_login(name, password):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name=%s AND password=%s"
    cursor.execute(query, (name, password))
    result = cursor.fetchone()
    conn.close()
    return result







