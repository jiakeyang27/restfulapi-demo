from models import get_db_connection
from config import Config
from utils.logger import get_logger

logger = get_logger(Config.APP_NAME)

def init_db():
    # Connect to the MySQL server
    conn = get_db_connection()

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create the users table if it does not exist
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_users_table)

    # Create the alarm_levels table if it does not exist
    create_alarm_levels_table = """
    CREATE TABLE IF NOT EXISTS alarm_levels (
        id INT AUTO_INCREMENT PRIMARY KEY,
        level VARCHAR(255) NOT NULL,
        description TEXT NOT NULL
    )
    """
    cursor.execute(create_alarm_levels_table)

    # Commit the changes
    conn.commit()

    # Print table info
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    logger.info(f"Tables: {tables}")

    # Close the cursor and connection
    cursor.close()
    conn.close()
    logger.info("Database initialization successful")
