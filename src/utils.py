
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
from psycopg2 import Error as PostgresError
from pandas.errors import DatabaseError

# Load environment variables
load_dotenv()

def get_database_connection():
    """
    Creates a connection to the database using environment variables.
    Returns a database connection object.
    Raises an exception if connection fails.
    """
    try:
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
    except PostgresError as e:
        raise Exception(f"Failed to connect to database: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error while connecting to database: {str(e)}")

def load_meditation_data():
    """
    Loads meditation data from the database into a pandas DataFrame.
    Returns a DataFrame containing meditation session data.
    Raises an exception if data loading fails.
    """
    conn = None
    try:
        conn = get_database_connection()
        df = pd.read_sql_query("SELECT * FROM meditation_sessions", conn)
        
        if df.empty:
            raise Exception("No meditation data found in database")
            
        return df
    
    except DatabaseError as e:
        raise Exception(f"Error reading data from database: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error while loading meditation data: {str(e)}")
    finally:
        if conn:
            conn.close()