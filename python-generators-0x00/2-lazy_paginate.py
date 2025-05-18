import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def paginate_users(page_size, offset):
    """Fetch a single page of users starting at a given offset."""
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def lazy_paginate(page_size):
    """Generator to lazily fetch pages of users from the database."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
