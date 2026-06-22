import mysql.connector
from mysql.connector import Error


def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change as per your MySQL username
            password=''  # Change as per your MySQL password
        )

        cursor = connection.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS heart_disease_db")
        print("Database created successfully!")

        # Use the database
        cursor.execute("USE heart_disease_db")

        # Create users table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           name
                           VARCHAR
                       (
                           100
                       ) NOT NULL,
                           email VARCHAR
                       (
                           100
                       ) UNIQUE NOT NULL,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                       """)

        # Create predictions table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS predictions
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           user_id
                           INT,
                           age
                           INT,
                           sex
                           INT,
                           cp
                           INT,
                           trestbps
                           INT,
                           chol
                           INT,
                           fbs
                           INT,
                           restecg
                           INT,
                           thalach
                           INT,
                           exang
                           INT,
                           oldpeak
                           FLOAT,
                           slope
                           INT,
                           ca
                           INT,
                           thal
                           INT,
                           risk_percentage
                           FLOAT,
                           prediction_result
                           VARCHAR
                       (
                           20
                       ),
                           prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY
                       (
                           user_id
                       ) REFERENCES users
                       (
                           id
                       )
                           )
                       """)

        print("Tables created successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_database()