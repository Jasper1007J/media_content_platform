import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

# Establishing the connection
load_dotenv()
def db_connect(merged_data):
    conn = mysql.connector.connect(
        host=os.getenv('HOSTNAME'),
        user=os.getenv('USERNAME'),
        password=os.getnev("PASSWORD")
    )

    # Creating a cursor object
    cursor = conn.cursor()

    # Creating a new database
    cursor.execute("CREATE DATABASE IF NOT EXISTS media_content;")

    print("Database Connected successfully!")

    # Selecting the database
    cursor.execute("USE media_content;")

    # Create category table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category(
            Category_id INT PRIMARY KEY AUTO_INCREMENT,
            Categories VARCHAR(100)
        );
    """)

    print("Category table created successfully")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS engagement(
            Engagement_id INT PRIMARY KEY AUTO_INCREMENT,
            Views BIGINT,
            Likes BIGINT,
            Comments INT,
            Engagement_rate FLOAT
        );
    """)

    print("Engagement table created successfully")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS date (
            Date_id INT PRIMARY KEY AUTO_INCREMENT,
            Date DATETIME,
            Day INT,
            Month INT,
            Year INT,
            Week VARCHAR(20)
        );
    """)




    print("Date table created successfully!")



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_data (
            Title_id INT PRIMARY KEY AUTO_INCREMENT,
            Source VARCHAR(50),
            Title TEXT,
            Date_id INT,
            Category_id INT,
            Engagement_id INT,
            FOREIGN KEY (Date_id) REFERENCES date(Date_id),
            FOREIGN KEY (Category_id) REFERENCES category(Category_id),
            FOREIGN KEY (Engagement_id) REFERENCES engagement(Engagement_id)
        );
    """)

    print("Created fact table successfully")




    for _, row in merged_data.iterrows():
        # Insert into date (if not exists)
        cursor.execute("""
            INSERT INTO date (Date, Day, Month, Year, Week)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Date_id = LAST_INSERT_ID(Date_id);
        """, (row["Date"], row["Day"], row["Month"], row["Year"], row["Week"]))
        date_id = cursor.lastrowid  # Get Date_id

        # Insert into category (if not exists)
        cursor.execute("""
            INSERT INTO category (Categories)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE Category_id = LAST_INSERT_ID(Category_id);
        """, (row["Categories"],))
        category_id = cursor.lastrowid  # Get Category_id

        # Insert into engagement
        cursor.execute("""
            INSERT INTO engagement (Views, Likes, Comments, Engagement_rate)
            VALUES (%s, %s, %s, %s)
        """, (row["Views"], row["Likes"], row["Comments"], row["Engagement_rate"]))
        engagement_id = cursor.lastrowid  # Get Engagement_id

        # Insert into fact_data
        cursor.execute("""
            INSERT INTO fact_data (Title, Source, Date_id, Category_id, Engagement_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (row["Title"], row["Source"], date_id, category_id, engagement_id))

    conn.commit()
    print("Data inserted successfully!")


    cursor.close()
    conn.close()
    print("Database connection closed successfully!")
