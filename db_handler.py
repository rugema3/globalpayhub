import os
import mysql.connector
from dotenv import load_dotenv

class Database:
    """
    A class for handling database operations using MariaDB.
    """
    def __init__(self):
        """
        Initialize the database connection using configuration from .env file.
        """
        load_dotenv() # load the environment variables
        host = os.getenv('DB_HOST')
        user =os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME')

        if not (host and user and password and database):
            raise ValueError("Database configuration not found in the .env file.")

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def close(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.conn.close()

    def execute_query(self, query, params=None):
        """
        Execute a SQL query.

        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to be used with the query.

        Returns:
            bool: True if the query was executed successfully, False otherwise.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            self.conn.rollback()
            return False

    def fetch_one(self, query, params=None):
        """
        Execute a SQL query and fetch a single row.

        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to be used with the query.

        Returns:
            dict: A dictionary representing a single row from the result.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            self.conn.rollback()
            return None


    def fetch_all(self, query, params=None):
        """
        Execute a SQL query and fetch all rows.

        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to be used with the query.

        Returns:
            list: A list of dictionaries representing rows from the result.
        """
        self.execute_query(query, params)
        return self.cursor.fetchall()



