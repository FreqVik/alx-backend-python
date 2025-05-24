import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the database connection and return the cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit if no exception, else rollback, and close the connection
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

# Use the context manager to perform a query
with DatabaseConnection('users.db') as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)