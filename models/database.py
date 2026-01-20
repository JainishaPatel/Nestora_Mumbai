from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

def db_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
)

def create_properties_table():
    db = db_connection()
    cursor = db.cursor(dictionary=True) 

    # sql = "CREATE DATABASE nestora"
    # sql = "SHOW DATABASES"
    sql = """
    CREATE TABLE IF NOT EXISTS properties(
        id CHAR(36) PRIMARY KEY,
        user_id CHAR(36) NOT NULL,

        title VARCHAR(255) NOT NULL,
        area VARCHAR(255) NOT NULL,
        direction VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        property_type VARCHAR(255) NOT NULL,
        bhk VARCHAR(255) NOT NULL,
        furnishing VARCHAR(255) NOT NULL,
        price INT NOT NULL,
        price_type VARCHAR(255) NOT NULL,
        images JSON NOT NULL,

        floor INT,
        total_floors INT,
        carpet_area INT,
        bathrooms INT,
        toilet_type VARCHAR(255),
        age_of_property INT,

        balcony TINYINT(1) DEFAULT 0,
        parking TINYINT(1) DEFAULT 0,
        lift TINYINT(1) DEFAULT 0,
        gas_pipeline TINYINT(1) DEFAULT 0,

        is_verified TINYINT(1) DEFAULT 0,
        is_available TINYINT(1) DEFAULT 1,

        water_supply VARCHAR(255),
        landmark VARCHAR(255),
        nearby_metro VARCHAR(255),
        nearby_school VARCHAR(255),
        nearby_hospital VARCHAR(255),

        owner_type VARCHAR(255),
        deposit INT,
        maintenance_charge INT,

        posted_on DATETIME DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id)
            REFERENCES users(user_id)
            ON DELETE CASCADE,

        INDEX idx_city (city),
        INDEX idx_price (price),
        INDEX idx_city_area (city, area)
    )
    """

    cursor.execute(sql)

    db.commit()
    cursor.close()
    db.close()


def create_users_table():
    db = db_connection()
    cursor = db.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS users(
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        phone VARCHAR(15) NULL,
        created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_login DATETIME DEFAULT NULL,
        is_active TINYINT(1) DEFAULT 1,
        is_admin TINYINT(1) DEFAULT 0,
        reset_token VARCHAR(255),
        reset_expires DATETIME
    )
    """

    cursor.execute(sql)
    
    db.commit()
    cursor.close()
    db.close()
    
if __name__ == "__main__":
    create_users_table()
    create_properties_table()
    