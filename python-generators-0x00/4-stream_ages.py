import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def stream_user_ages():
    """Generator to yield user ages one by one."""
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    """Compute average age using the generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
        print(f"Total number of users: {count}")


if __name__ == "__main__":
    compute_average_age()
