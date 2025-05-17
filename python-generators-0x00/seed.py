import os
import mysql.connector
from dotenv import load_dotenv
import uuid
import csv
load_dotenv()

url = os.getenv("DATABASE_URL")
if url is None:
    raise ValueError("DATABASE_URL environment variable not set")


def connect_db():
    """Connect to the database."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )

def create_database(connection):
    """Creates the database"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    """Connect to the database and create the database if it doesn't exist."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev"
    )
    

def create_table(connection):
    """Create the table in the database."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        )
    """)
    connection.commit()
    cursor.close()

def insert_data(connection, data):
    """Insert data into the table."""
    cursor = connection.cursor()
    insert_query = ("""
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
    """)
    records = []
    with open(data, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = float(row['age'])  # convert age to float
            records.append((user_id, name, email, age))

    cursor.executemany(insert_query, records)
    connection.commit()
    cursor.close()
    connection.commit()
    cursor.close()